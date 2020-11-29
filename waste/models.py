from django.db import models
from django.conf import settings

#from .main import generate_waste_rep 

import json




class WasteClass(models.Model):

    name = models.CharField(max_length=1000, blank=False, verbose_name="Название отхода")
    components = models.ManyToManyField('chemcomponent.WasteComponent', through='waste.ConcentrationClass')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,)
    fkko = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код ФККО")
    #visibility = models.BooleanField(default=False, blank=False, null=False, verbose_name="Отход виден всем")

    def get_safe_components(self):
        query = self.components.filter(chemical_type = "S")
        return list(query.values('name'))


    def generate_report(self):
        data={}
        data['name'] = self.name
        data['fkko'] = self.fkko
        data['safety_class'] = self.get_safety_class()
        data["k"] = "%.2f" % self.get_summ_K()
        data["components"] = {}
        data["filename"] = self.pk

        for concentration in self.concentrations.all():
            data["components"][concentration.component.name]= \
                                {   "concp": "%.2f" % concentration.conc_p , 
                                    "concr": "%.2f" % concentration.conc_value, 
                                    "xi": "%.2f" % concentration.component.get_x(), 
                                    "zi": "%.2f" % concentration.component.get_z(), 
                                    "lgw": "%.2f" % concentration.component.get_log_w(), 
                                    "w": "%.2f" % concentration.component.get_w(), 
                                    "k": "%.2f" % concentration.get_K(),
                                    "props": concentration.component.get_props(),
                                }
        #data["safe_components"] = self.get_safe_components() 



        context = json.dumps(data,ensure_ascii=False).encode('utf8')
        #generate_waste_rep(context = context)

    def get_summ_K(self, fake_objs):

        k=0
        if fake_objs:
            concentrations=fake_objs
        else:
            concentrations=self.concentrations.all()
        
        for component in concentrations:
            k += component.get_K()        
        return k
    
    def get_safety_class(self, fake_objs=False):

               

        k = self.get_summ_K(fake_objs=fake_objs)
        if k == 1:
            return "V"
        elif 1 < k <= 100:
            return "IV"
        elif 100 < k <= 1000:
            return "III"
        elif 1000 < k <= 10000:
            return "II"
        else:
            return "I"
          


class ConcentrationClass(models.Model):

    waste = models.ForeignKey(WasteClass, on_delete=models.CASCADE, related_name="concentrations")
    component = models.ForeignKey('chemcomponent.WasteComponent', on_delete=models.CASCADE, related_name="concentrations")
    conc_value = models.FloatField(blank=False, null=False)
    conc_p = models.FloatField(blank=False, null=False, default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,)

    class Meta:
        unique_together = ['waste', 'component']


    def get_K(self):

        return self.component.get_k(self.conc_value)
