from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

import math


class WasteComponent(models.Model):
    """
    class for a component of the waste
    Класс для компонентов отхода
    """    
    name = models.CharField(max_length=400, blank=False, verbose_name="Название")
    other_names = models.CharField(max_length=1000, blank=True, default="", verbose_name="Другие названия (через запятую)")
    CHOICES = (        
        ('O', 'Органическое'),
        ('I', 'Неорганическое'),          
    )

    chemical_type = models.CharField(max_length=1, 
                                     blank=False, 
                                     default = 'O', 
                                     choices=CHOICES, 
                                     verbose_name="Тип")
    w_value = models.FloatField(blank=True, 
                                null=True, 
                                verbose_name="W - Коэффициента степени опасности компонента (если известен - указание источника обязательно)",
                                validators=[MinValueValidator(1.0),MaxValueValidator(1e6)])
    lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='waste_components', 
                                    verbose_name='Источник литературы (если задано числовое значение W, то обязателен)')
    
    cas_number = models.CharField(max_length=30,
                                  verbose_name="Регистрационный номер CAS",
                                  blank=True,
                                  validators=[RegexValidator(regex=r"\b[1-9]{1}[0-9]{1,6}-\d{2}-\d\b",
                                                             message="CAS код для вещества в формате 1111-11-1"),
                                             ]
                                 )

    

    def get_props(self):
        """
        returns array of all props in {'prop': value} format
        """

        if not self.value_props.exists() and not self.category_props.exists():
            return {}
        
        props = {}
        for prop in self.value_props.all():
            data = prop.get_json()
            props[data['name']]=data["data"]

        for prop in self.category_props.all():
            data = prop.get_json()
            props[data['name']]=data["data"]

        return props

    
  
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
        если значение w задано в базе возвращает значение из базы
        """      
        if self.w_value:
            return self.w_value

        return 10.**self.get_log_w()
    
    def get_log_w(self):
        """
        Функция считает логарифм от коэффициента степени опасности компонента
        уточнить логарифм десятичный или какой-то другой
        """      

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
        if self.w_value:
            return self.get_log_w()
        return 4./3.*self.get_x()-1./3.
    
    def get_x(self):
        """
        относительный параметр опасности компонента отхода для окружающей среды
        """ 

        if self.w_value:
            if self.w_value == 1000000:
                return 4.
            return (self.get_z()+1./3.)*3./4.

        BigX = 0
        num_props = 0     
       
        for value_prop in self.value_props.all():           
            BigX += value_prop.get_score()
            num_props += 1
                
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
    
    def Binf(self):
        """
        Бал за информационное обеспечение
        """

        cat_props_num = self.category_props.count()
        val_props_num = self.value_props.count()
        
        num_props = cat_props_num + val_props_num

        if num_props < 6:
            Binf = 1
        elif 6 <= num_props <= 8:
            Binf = 2
        elif 8 < num_props <= 10:
            Binf = 3
        else:
            Binf = 4
        
        return Binf


    def __str__(self):
        return f'{self.name} ({self.get_chemical_type_display()})'
    
    def clean(self):
        if self.w_value and not self.lit_source:
            raise ValidationError(f'При задании коэффициента W, необходимо указать источник литературы, откуда он взят')      
    
    class Meta:
        verbose_name = "Компонент отхода"
        verbose_name_plural = "Компоненты отхода"



