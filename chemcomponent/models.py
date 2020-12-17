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
    other_names = models.CharField(max_length=1000, blank=True, default="", verbose_name="Другие названия (через точку с запятой)")
    cas_number = models.CharField(max_length=30,
                                  verbose_name="Регистрационный номер CAS",
                                  blank=True,
                                  validators=[RegexValidator(regex=r"\b[1-9]{1}[0-9]{1,6}-\d{2}-\d\b",
                                                             message="CAS код для вещества в формате 1111-11-1"),
                                             ]
                                 )
    CHOICES = (        
        ('O', 'Органическое'),
        ('I', 'Неорганическое'),          
    )
    chemical_type = models.CharField(max_length=1, 
                                     blank=False, 
                                     default = 'O', 
                                     choices=CHOICES, 
                                     verbose_name="Тип")

    x_value = models.FloatField(blank=True, 
                                null=True, 
        verbose_name="X - относительный параметр опасности компонента отхода для окружающей среды (если известен - указание источника обязательно)",
                                validators=[MinValueValidator(1.0),MaxValueValidator(4.0)])
    x_value_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='x_value', 
                                    verbose_name='Источник литературы для относительного параметра опаности (если задано числовое значение X, то обязателен)')
                               

    land_concentration = models.FloatField(blank=True, 
                                null=True, 
                                verbose_name="Максимальная фоновая концентрация в почвах (мг/кг) (если известно - указание источника обязательно)",
                                validators=[MinValueValidator(0), MaxValueValidator(1e6)])
    
    land_concentration_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='land_concentration', 
                                    verbose_name='Источник литературы для фоновой концентрации (если задана фоновая концентрация, то обязателен)')
   
    
    s_rastv = models.FloatField(blank=True, 
                                null=True, 
                                verbose_name="Растворимость компонента отхода (вещества) в воде при 20°С (мг/л)",
                                validators=[MinValueValidator(0)])
    
    s_rastv_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='s_rastv', 
                                    verbose_name='Источник литературы для растворимости компонента отхода (если задана, то обязателен)')

    pdk_v = models.FloatField(blank=True, 
                                null=True, 
    verbose_name="Предельно допустимая концентрация вещества в воде водных объектов, используемых для целей питьевого и хозяйственно-бытового водоснабжения (мг/л)",
                                validators=[MinValueValidator(0)])
    
    pdk_v_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='pdk_v', 
                                    verbose_name='Источник литературы для ПДКв (если задан, то обязателен)')

   
    c_nasish = models.FloatField(blank=True, 
                                null=True, 
                                verbose_name="Насыщающая концентрация вещества в воздухе при 20°С и нормальном давлении (мг/м^3)",
                                validators=[MinValueValidator(0)])
    
    c_nasish_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='c_nasish', 
                                    verbose_name='Источник литературы для насыщающей концентрации вещества (если задана, то обязателен)')

   
    pdk_rz = models.FloatField(blank=True, 
                                null=True, 
                verbose_name="Предельно допустимая концентрация вещества в атмосферном воздухе рабочей зоны (мг/м^3)",
                                validators=[MinValueValidator(0)])
    
    pdk_rz_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='pdk_rz', 
                                    verbose_name='Источник литературы для ПДКрз (если задан, то обязателен)')


    pdk_ss = models.FloatField(blank=True, 
                                null=True, 
                verbose_name="Предельно допустимая концентрация вещества среднесуточная в атмосферном воздухе населенных мест (мг/м^3)",
                                validators=[MinValueValidator(0)])
    
    pdk_ss_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='pdk_ss', 
                                    verbose_name='Источник литературы для ПДКсс (если задан, то обязателен)')


    pdk_mr = models.FloatField(blank=True, 
                                null=True, 
                verbose_name="Предельно допустимая концентрация вещества максимально разовая в атмосферном воздухе населенных мест (мг/м^3)",
                                validators=[MinValueValidator(0)])
    
    pdk_mr_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='pdk_mr', 
                                    verbose_name='Источник литературы для ПДКмр (если задан, то обязателен)')
    
    bpk5 = models.FloatField(blank=True, 
                            null=True, 
                verbose_name="Биологическое потребление кислорода, выраженное в миллилитрах O2/л за 5 суток",
                            validators=[MinValueValidator(0)])
    
    bpk5_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='bpk5', 
                                    verbose_name='Источник литературы для БПК5 (если задан, то обязателен)')


    xpk = models.FloatField(blank=True, 
                                null=True, 
                verbose_name="Химическое потребление кислорода ХПК, выраженное в миллилитрах O2/100 л",
                                validators=[MinValueValidator(0)])
    
    xpk_lit_source = models.ForeignKey('litsource.LiteratureSource',
                                    blank=True, 
                                    null=True, 
                                    on_delete=models.SET_NULL, 
                                    related_name='xpk', 
                                    verbose_name='Источник литературы для ХПК (если задан, то обязателен)')


    def get_pdk_v_score(self):  

        if not self.pdk_v:
            return 0
        if self.pdk_v > 1:
            return 4
        elif 0.1 < self.pdk_v <= 1 :
            return 3
        elif 0.01 <= self.pdk_v <= 0.1:
            return 2
        return 1

    def get_BD_score(self):
        if not self.bpk5 or not self.xpk:
            return [False, 0]
        bd = self.bpk5 / self.xpk *100
        
        if bd > 10:
            return [bd, 4]
        elif 1 < bd <= 10:
            return [bd, 3]
        elif 0.1 <= bd <= 1:
            return [bd, 2]
        return [bd, 1]
    
   # def get_lg_



    def get_x(self):
        """
        относительный параметр опасности компонента отхода для окружающей среды
        """
        if self.x_value:
            return self.x_value 

        BigX = self.get_pdk_v_score() + self.get_BD_score()[1]
          
       
        for value_prop in self.value_props.all():           
            BigX += value_prop.get_score()
            
                
        for category_prop in self.category_props.all():
            BigX += category_prop.get_score()
            
            

        Binf = self.Binf()[0]
        num_props = self.Binf()[1]
                    
        return (BigX + Binf) / (num_props + 1)
    
    def get_z(self):
        """
        унифицированный относительный параметр опасности компонента отхода для окружающей среды
        """        
        return 4./3.*self.get_x()-1./3.
    
    def get_log_w(self):
        """
        Функция считает логарифм от коэффициента степени опасности компонента
        уточнить логарифм десятичный или какой-то другой
        """        

        z = self.get_z()
        if 1. <= z <= 2:
            return 4. - 4. / z
        elif 2. < z <= 4:
            return z
        elif 4. < z <= 5:
            return 2. + 4. / (6 - z)

        return 1
    
    def get_w(self):
        """
        Функция считает коэффициента степени опасности компонента       
        если значение w задано в базе возвращает значение из базы
        """           

        return 10.**self.get_log_w()
    
  
    def get_k(self, conc):
        """
        Показатель опасности компонента отхода 
        conc - концентрация в мг/кг
        если для компонента задана фоновая концентрация в почве и значение conc меньше нее
        принимает W=1e6
        в противном случае считает W согласно методике по свойства
        """
        if self.land_concentration:
            if conc > self.land_concentration:
                return conc / self.get_w()
            return conc/1e6
        return conc / self.get_w()
    
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
    
    def Binf(self):
        """
        Бал за информационное обеспечение
        """

        cat_props_num = self.category_props.count()
        val_props_num = self.value_props.count()        
        num_props = cat_props_num + val_props_num

        props_1_num = ['pdk_v', 'pdk_ss', 'pdk_mr', ]
        for prop in props_1_num:
            if bool(eval(f'self.{prop}')):
                num_props += 1
        pair_props = [ ['bpk5', 'xpk',], ['s_rastv', 'pdk_v',], ['c_nasish', 'pdk_rz'], ['c_nasish', 'pdk_ss'], ['c_nasish', 'pdk_mr']]
        
        for pair in pair_props:
            if bool(eval(f'self.{pair[0]}')) and bool(eval(f'self.{pair[1]}')):
                num_props += 1

        if num_props < 6:
            Binf = 1
        elif 6 <= num_props <= 8:
            Binf = 2
        elif 8 < num_props <= 10:
            Binf = 3
        else:
            Binf = 4
        
        return [Binf, num_props]


    def __str__(self):
        return f'{self.name} ({self.get_chemical_type_display()})'
    
    def clean(self):

        props = ['x_value', 'land_concentration', 's_rastv', 'pdk_v', 'c_nasish', 'pdk_rz', 'pdk_ss', 'pdk_mr', 'bpk5', 'xpk']

        for prop_str in props:
            prop = bool(eval(f'self.{prop_str}'))
            prop_source = bool(eval(f'self.{prop_str}_lit_source'))
            if prop and not prop_source:
                raise ValidationError(f'При задании свойства {prop_str} необходимо задать источник')
            if not prop and prop_source:
                raise ValidationError(f'Для свойства {prop_str} задан источник, но не задано значение')


        
    
    class Meta:
        verbose_name = "Компонент отхода"
        verbose_name_plural = "Компоненты отхода"


