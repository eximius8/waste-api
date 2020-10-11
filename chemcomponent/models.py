from django.db import models

from django.core.exceptions import ValidationError

class LiteratureSource(models.Model):

    name = models.CharField(blank=False, max_length=100, unique=True)
    latexpart = models.TextField(blank=False)

    def __str__(self):
        return self.name



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

    def get_num_unique_props(self):
        """
        get number of hazard_props with unique prop_types
        should be updated to distinct
        """
        x = set()
        for prop in self.properties.all():
            x.add(prop.prop_type)        
        if len(x) < 6:
            Binf = 1
        elif 6 <= len(x) <= 8:
            Binf = 2
        elif 8 < len(x) <= 10:
            Binf = 3
        else:
            Binf = 4

        return [len(x), Binf]
   
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

        return 10.**self.get_log_w()
    
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
        x = set()
        for prop in self.properties.all():
            if not prop.prop_type in x:                
                x.add(prop.prop_type)
                BigX += prop.get_score()
        if len(x) < 6:
            Binf = 1
        elif 6 <= len(x) <= 8:
            Binf = 2
        elif 8 < len(x) <= 10:
            Binf = 3
        else:
            Binf = 4
                    
        return (BigX + Binf) / (len(x) + 1)


    def __str__(self):
        return f'{self.name} ({self.get_chemical_type_display()})'
    
    class Meta:
        verbose_name = "Компонент отхода"
        verbose_name_plural = "Компоненты отхода"


class HazardValueType(models.Model):
    name = models.CharField(max_length=400, blank=False, verbose_name="Название")

    bad_val = models.FloatField(blank=False, verbose_name="Значение выше или меньше которого класс опасности = 1")
    average_val = models.FloatField(blank=False, verbose_name="Среднее значение")
    good_val = models.FloatField(blank=False, verbose_name="Значение выше или меньше которого класс опасности = 4")

    def get_score(self, obj_value):
        if good_val < bad_val:
            if obj_value < good_val:
                return 4
            elif obj_value > bad_val:
                return 1
            elif good_val <= obj_value <= average_val:
                return 3
            elif average_val < obj_value <= bad_val:
                return 2

        if obj_value > good_val:
            return 4
        elif obj_value < bad_val:
            return 1
        elif average_val <= obj_value <= good_val:
            return 3
        elif bad_val < obj_value <= average_val:
            return 2


    def clean(self):
        if good_val < bad_val and (average_val < good_val or average_val > bad_val):
            raise ValidationError(f'Среднее значение должно быть между {self.good_val} и {self.bad_val}')
        
        if bad_val < good_val and (average_val < bad_val or average_val > good_val):
            raise ValidationError(f'Среднее значение должно быть между {self.bad_val} и {self.good_val}')
   

class AbstractHazardProp(models.Model):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE, related_name='properties')
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE, related_name='properties')
    importance = models.PositiveSmallIntegerField(blank=False,                                                 
                                                 verbose_name='Важность')

    class Meta:
        abstract = True

class HazardValueProp(AbstractHazardProp):

    value_type = models.ForeignKey(HazardValueType, on_delete=models.CASCADE, related_name='properties')
    
    CHOICES = (
        (1, 'ПДК (ОДК) в почве, мг/кг'), 
        (2, 'ПДК (ОДУ) в воде, мг/л'),
        (3, 'ПДК рабочей зоны, мг/м^3'),
        (4, 'ПДК среднесуточная или максимально разовая (ОБУВ), мг/м^3'),
        (5, 'Класс опасности в воде'),
        (6, 'Класс опасности в рабочей зоне'),
        (7, 'Класс опасности в атмосферном воздухе'),
        (8, 'Класс опасности в почве'),   
        (9, 'DL50 перорально, мг/кг'),
        (10, 'CL50, мг/м^3'),
        (11, 'Канцерогенность'),
        (12, 'Lg (S, мг/л/ПДКв)'),
        (13, 'Lg (Снас, мг/м^3/ПДКр. з)'),
        (14, 'ПДКвр, мг/л'),
        (15, 'DL50skin, мг/кг '),
        (16, 'CL50w, мг/л/96 ч '),
        (17, 'Lg (Снас, мг/м^3/ПДКсс/мр)'),
        (18, 'КВИО'),
        (19, 'Log Kow (октанол/вода)'),
        (20, 'Персистентность: трансформация в окружающей среде'),
        (21, 'Биоаккумуляция: поведение в пищевой цепочке'),
        (22, 'Мутагенность'),
        (23, 'ПДКпп в продуктах питания'),                  
    )

    allowed_ranges = {
        1: (5., 50.5, 1000., ), 
        2: (0.01, 0.105, 1., ),
        3: (0.1, 1.05, 10., ),
        4: (0.01, 0.105, 1., ),  
        9: (15., 150.5, 5000., ),
        10: (500, 5000.5, 50000., ),
        12: (5., 1.95, 1.),
        13: (5., 1.95, 1.),
        14: (0.001, 0.0105, 0.1, ),
        15: (0.001, 0.0105, 0.1, ),
        16: (0.001, 0.0105, 0.1, ),
        17: (0.001, 0.0105, 0.1, ),
        18: (0.001, 0.0105, 0.1, ),
        19: (0.001, 0.0105, 0.1, ),
        23: (0.001, 0.0105, 0.1, )           
    }

    CLASS_CHOICES = (     
        (1, '1 класс'),
        (2, '2 класс'),
        (3, '3 класс'),
        (4, '4 класс'),            
    )

    CANCEROG_CHOICES = (     
        (1, 'Доказана для человека'),
        (2, 'Доказана для животных'),
        (3, 'Есть вероятность для животных'),
        (4, 'Неканцероген (доказано)'),            
    )

    PERSIST_CHOICES = (     
        (1, 'Образование болеетоксичных продуктов, в т.ч. обладающих отдаленными эффектами или новыми свойствами'),
        (2, 'Образование продуктов с более выраженным влиянием др. критериев вредности'),
        (3, 'Образование продуктов, токсичность которых близка к токсичности исходного вещества'),
        (4, 'Образование менее токсичных продуктов'),            
    )

    BIOACC_CHOICES = (     
        (1, 'Накопление во всех звеньях'),
        (2, 'Накопление в нескольких звеньях'),
        (3, 'Накопление в одном из звеньев'),
        (4, 'Нет накопления'),            
    )

    MUTAG_CHOICES = (     
        (1, 'Обнаружена'),
        (2, 'Есть возможность проявления для человека'),
        (3, 'Есть возможность проявления для животных'),
        (4, 'Отсутствует (доказано)'),            
    )

    prop_type = models.PositiveSmallIntegerField(blank=False, 
                                                 choices=CHOICES,
                                                 verbose_name='Тип свойства')
    prop_float_value = models.FloatField(blank=True, 
                                         null=True,
                                         verbose_name='Числовое значение')
    prop_class_value = models.PositiveSmallIntegerField(blank=True, 
                                                        null=True, 
                                                        choices=CLASS_CHOICES,
                                                        verbose_name='Класс опасности')
    prop_cancerog_value = models.PositiveSmallIntegerField(blank=True, 
                                                           null=True, 
                                                           choices=CANCEROG_CHOICES,
                                                           verbose_name='Канцерогенность')
    prop_presist_value = models.PositiveSmallIntegerField(blank=True, 
                                                          null=True, 
                                                          choices=PERSIST_CHOICES,
                                                          verbose_name='Персистентность: трансформация в окружающей среде')
    prop_bioacc_value = models.PositiveSmallIntegerField(blank=True, 
                                                         null=True, 
                                                         choices=BIOACC_CHOICES,
                                                         verbose_name='Биоаккумуляция: поведение в пищевой цепочке')

    prop_mutag_value = models.PositiveSmallIntegerField(blank=True, 
                                                         null=True, 
                                                         choices=MUTAG_CHOICES,
                                                         verbose_name='Мутагенность')                                                    

    def get_val(self):
        is_numeric = self.prop_type in [1,2,3,4,9,10,12,13,14,15,16,17,18,19,23]
        is_class = self.prop_type in [5,6,7,8]
        is_cancerog = self.prop_type in [11]
        is_presist = self.prop_type in [20]
        is_bioacc = self.prop_type in [21]
        is_mutag = self.prop_type in [22]
        if is_numeric:
            return self.prop_float_value
        elif is_class:
            return self.get_prop_class_value_display()
        elif is_cancerog:
            return self.get_prop_cancerog_value_display()
        elif is_presist:
            return self.get_prop_presist_value_display()
        elif is_bioacc:
            return self.get_prop_bioacc_value_display()
        elif is_mutag:
            return self.get_prop_mutag_value_display()
        
    
    def get_score(self):

        if self.prop_type in [5,6,7,8]:
            return self.prop_class_value
        elif self.prop_type == 11:
            return self.prop_cancerog_value
        elif self.prop_type == 20:
            return self.prop_presist_value
        elif self.prop_type == 21:
            return self.prop_bioacc_value
        elif self.prop_type == 22:
            return self.prop_mutag_value

        allowed_range = self.allowed_ranges[self.prop_type]
        if allowed_range[0] < allowed_range[2]:
            if self.prop_float_value < allowed_range[0]:
                return 1
            elif allowed_range[0] <= self.prop_float_value <= allowed_range[1]:
                return 2
            elif allowed_range[1] <= self.prop_float_value <= allowed_range[2]:
                return 3
            else:
                return 4
        elif allowed_range[0] > allowed_range[2]:
            if self.prop_float_value > allowed_range[0]:
                return 1
            elif allowed_range[0] >= self.prop_float_value >= allowed_range[1]:
                return 2
            elif allowed_range[1] >= self.prop_float_value >= allowed_range[2]:
                return 3
            else:
                return 4
        


    def clean(self):

        is_numeric = self.prop_type in [1,2,3,4,9,10,12,13,14,15,16,17,18,19,23]
        is_class = self.prop_type in [5,6,7,8]
        is_cancerog = self.prop_type in [11]
        is_presist = self.prop_type in [20]
        is_bioacc = self.prop_type in [21]
        is_mutag = self.prop_type in [22]

        if is_numeric:            
            self.prop_class_value = None
            self.prop_cancerog_value = None
            self.prop_presist_value = None
            self.prop_bioacc_value = None
            self.prop_mutag_value = None
        if is_class:
            self.prop_float_value = None            
            self.prop_cancerog_value = None
            self.prop_presist_value = None
            self.prop_bioacc_value = None
            self.prop_mutag_value = None
            
        if is_cancerog:
            self.prop_float_value = None
            self.prop_class_value = None            
            self.prop_presist_value = None
            self.prop_bioacc_value = None
            self.prop_mutag_value = None
        if is_presist:
            self.prop_float_value = None
            self.prop_class_value = None
            self.prop_cancerog_value = None            
            self.prop_bioacc_value = None
            self.prop_mutag_value = None
        if is_bioacc:
            self.prop_float_value = None
            self.prop_class_value = None
            self.prop_cancerog_value = None
            self.prop_presist_value = None            
            self.prop_mutag_value = None
        if is_mutag:
            self.prop_float_value = None
            self.prop_class_value = None
            self.prop_cancerog_value = None
            self.prop_presist_value = None
            self.prop_bioacc_value = None            

        if is_class and not self.prop_class_value:
            raise ValidationError(f'Для "{self.get_prop_type_display()}" должен быть выбран класс опасности')

        if is_cancerog and not self.prop_cancerog_value:
            raise ValidationError(f'Выберете канцерогенность')

        if is_presist and not self.prop_presist_value:
            raise ValidationError(f'Выберете Персистентность')
              
        if is_bioacc and not self.prop_bioacc_value:
            raise ValidationError(f'Выберете Биоаккумуляцию')
        
        if is_mutag and not self.prop_mutag_value:
            raise ValidationError(f'Выберете Мутагенность')

        if is_numeric and not self.prop_float_value:
            raise ValidationError(f'Для "{self.get_prop_type_display()}" должно быть установлено числовое значение')

        if is_numeric and self.prop_float_value < 0 and self.prop_type != 19:     
            raise ValidationError(f'{self.get_prop_type_display()} не может быть меньше 0')

    

    def __str__(self):
        return self.get_prop_type_display()
       
 


