from django.db import models
from django.conf import settings



class WasteClass(models.Model):

    name = models.CharField(max_length=1000, blank=False, verbose_name="Название отхода")
    components = models.ManyToManyField('chemcomponent.WasteComponent', through='waste.Concentration')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,)
    #visibility = models.BooleanField(default=False, blank=False, null=False, verbose_name="Отход виден всем")

    def get_summ_K(self):
        
        k=0
        for component in self.concentrations.all():
            k += component.get_K()        
        return k
    
    def get_safety_class(self):

        k = self.get_summ_K()
        if k <= 10:
            return 5
        elif 10 < k <= 100:
            return 4
        elif 100 < k <= 1000:
            return 3
        elif 1000 < k <= 10000:
            return 2
        else:
            return 1
          


class Concentration(models.Model):

    waste = models.ForeignKey(WasteClass, on_delete=models.CASCADE, related_name="concentrations")
    component = models.ForeignKey('chemcomponent.WasteComponent', on_delete=models.CASCADE, related_name="concentrations")
    conc_value = models.FloatField(blank=False, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,)

    class Meta:
        unique_together = ['waste', 'component']


    def get_K(self):

        return self.component.get_k(self.conc_value)
