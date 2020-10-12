from django.db import models
from django.core.exceptions import ValidationError

import math


class WasteComponent(models.Model):
    """
    class for a component of the waste
    Класс для компонентов отхода
    """    
    name = models.CharField(max_length=400, blank=False, verbose_name="Название")
    CHOICES = (
        ('S', 'Неопасное W=10^6'), 
        ('O', 'Органическое'),
        ('I', 'Неорганическое'),          
    )

    chemical_type = models.CharField(max_length=1, 
                                     blank=False, 
                                     default = 'S', 
                                     choices=CHOICES, 
                                     verbose_name="Тип")
    w_value = models.FloatField(blank=True, 
                                null=True, 
                                verbose_name="W - Коэффициента степени опасности компонента (если известен - указание источника обязательно)")
    lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='waste_components', 
                                    verbose_name='Источник литературы (если задано числовое значение W, то обязателен)')

    def clean(self):
        if self.w_value and not self.lit_source:
            raise ValidationError(f'При задании коэффициента W, необходимо указать источник литературы, откуда он взят')      

                           
    

    def get_num_unique_props(self):
        """
        get number of hazard_props with unique importances
        should be updated to distinct
        """       
        prop_num = self.category_props.count() + self.value_props.count()
           
        if prop_num < 6:
            Binf = 1
        elif 6 <= prop_num <= 8:
            Binf = 2
        elif 8 < prop_num <= 10:
            Binf = 3
        else:
            Binf = 4

        return [prop_num, Binf]
   
    def get_k(self, conc):
        """
        Показатель опасности компонента отхода 
        conc - концентрация в мг/кг
        """
        return conc/self.get_w()


    def get_w(self):
        """
        Функция считает коэффициента степени опасности компонента
        если компонент безопасен возвращает 10^6
        """
        if self.chemical_type == 'S':
            return 1000000.
        if self.w_value:
            return self.w_value


        return 10.**self.get_log_w()
    
    def get_log_w(self):
        """
        Функция считает логарифм от коэффициента степени опасности компонента
        уточнить логарифм десятичный или какой-то другой
        """
        if self.chemical_type == 'S':

            return 6.
        if self.w_value:
            return math.log10(self.w_value)

        z = self.get_z()
        if 1. <= z <= 2:
            return 4. - 4. / z
        elif 2. < z <= 4:
            return z
        elif 4. < z <= 5:
            return -2. + 4. / (6 - z)

        return 1

    def get_z(self):
        """
        унифицированный относительный параметр опасности компонента отхода для окружающей среды
        """
        return 4./3.*self.get_x()-1./3.
    
    def get_x(self):
        """
        относительный параметр опасности компонента отхода для окружающей среды
        """
        BigX = 0
        num_props = 0     
       
        for value_prop in self.value_props.all():
            BigX += value_prop.get_score()
            num_props += 1
            # if not value_prop.value_type.importance in x:                
            #     x.add(value_prop.value_type.importance)
                
        for category_prop in self.category_props.all():
            BigX += category_prop.get_score()
            num_props += 1
            

        if num_props < 6:
            Binf = 1
        elif 6 <= num_props <= 8:
            Binf = 2
        elif 8 < num_props <= 10:
            Binf = 3
        else:
            Binf = 4
                    
        return (BigX + Binf) / (num_props + 1)


    def __str__(self):
        return f'{self.name} ({self.get_chemical_type_display()})'
    
    class Meta:
        verbose_name = "Компонент отхода"
        verbose_name_plural = "Компоненты отхода"



