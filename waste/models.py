from django.db import models
from django.conf import settings

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


    def generate_report(self, fake_objs, filename):
        data={}
        data['name'] = self.name
        data['fkko'] = ""# self.fkko
        data['safety_class'] = self.get_safety_class(fake_objs)
        data["k"] = "%.2f" % self.get_summ_K(fake_objs)
        data["components"] = {}
        data["filename"] = filename

        for concentration in fake_objs:
            
            data["components"][concentration.component.name]= \
                                {   "concp": float(concentration.conc_value * 1e-4), #"%.2f" % 
                                    "concr": "%.0f" % concentration.conc_value, 
                                    "xi": "%.2f" % concentration.component.get_x(), 
                                    "zi": "%.2f" % concentration.component.get_z(), 
                                    "lgw": "%.2f" % concentration.component.get_log_w(), 
                                    "w": "%.0f" % concentration.component.get_w(), 
                                    "k": "%.1f" % concentration.get_K(),
                                    "props": concentration.component.get_props(),
                                    "has_x": bool(concentration.component.x_value),
                                    "has_soil_c": bool(concentration.component.land_concentration),
                                }
        #data["safe_components"] = self.get_safe_components()
        context = json.dumps(data,ensure_ascii=False).encode('utf8')
        import requests
        #url = 'https://us-central1-bezoder.cloudfunctions.net/safety-report/'
        url = 'http://0.0.0.0:8080/'
        data = context
        response = requests.post(url, data=data)
        return response

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
        if k <= 10:
            return "V"
        elif 10 < k <= 100:
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
