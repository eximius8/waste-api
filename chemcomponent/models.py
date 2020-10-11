from django.db import models

from django.core.exceptions import ValidationError

class LiteratureSource(models.Model):

    name = models.CharField(blank=False, max_length=100, unique=True)
    latexpart = models.TextField(blank=False)



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

    hazard_value_prop = models.ManyToManyField(LiteratureSource, 
                                         through='HazardValueProp', 
                                         #verbose_name="Числовой показатель опасности",
                                         related_name='hazard_value_prop',
                                         )
                                        
    hazard_class_prop = models.ManyToManyField(LiteratureSource, 
                                         through='HazardClassProp', 
                                        # verbose_name="Класс опасности"
                                        related_name='hazard_class_prop',
                                        )

    cancerog_prop = models.ManyToManyField(LiteratureSource, 
                                         through='CancerogProp', 
                                        # verbose_name="Канцерогенность"
                                        related_name='cancerog_prop',
                                        )

    persist_prop = models.ManyToManyField(LiteratureSource, 
                                         through='PersistProp', 
                                         #verbose_name="Персистентность"
                                         related_name='persist_prop',
                                         )

    bio_acc_prop = models.ManyToManyField(LiteratureSource, 
                                         through='BioAccProp', 
                                        # verbose_name="Биоаккумуляция"
                                        related_name='bio_acc_prop',
                                         )                                     

    mutagen_prop = models.ManyToManyField(LiteratureSource, 
                                         through='MutagenProp', 
                                        # verbose_name="Мутагенность"
                                        related_name='mutagen_prop',
                                         )

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

        return 0

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Компонент отхода"



class HazardAbstractProp(models.Model):

    def get_score(self):
        return self.prop_value

    def get_prop_type(self):
        return self.prop_type 

    class Meta:
        abstract = True       

class HazardValueProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    
    CHOICES = (
        (1, 'ПДК (ОДК) в почве, мг/кг'), 
        (2, 'ПДК (ОДУ) в воде, мг/л'),
        (3, 'ПДК рабочей зоны, мг/м^3'),
        (4, 'ПДК среднесуточная или максимально разовая (ОБУВ), мг/м^3'),      
        (9, 'DL50 перорально, мг/кг'),
        (10, 'CL50, мг/м^3'),
        (12, 'Lg (S, мг/л/ПДКв)'),
        (13, 'Lg (Снас, мг/м^3/ПДКр. з)'),
        (14, 'ПДКвр, мг/л'),
        (15, 'DL50skin, мг/кг '),
        (16, 'CL50w, мг/л/96 ч '),
        (17, 'Lg (Снас, мг/м^3/ПДКсс/мр)'),
        (18, 'КВИО'),
        (19, 'Log Kow (октанол/вода)'),     
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

    prop_type = models.PositiveSmallIntegerField(blank=False, choices=CHOICES)
    prop_value = models.FloatField(blank=False)

    def get_score(self):
        allowed_range = self.allowed_ranges[self.prop_type]
        if allowed_range[0] < allowed_range[2]:
            if self.prop_value <= allowed_range[0]:
                return 1
            elif allowed_range[0] <= self.prop_value <= allowed_range[1]:
                return 2
            elif allowed_range[1] <= self.prop_value <= allowed_range[2]:
                return 3
            else:
                return 4
        elif allowed_range[0] > allowed_range[2]:
            if self.prop_value >= allowed_range[0]:
                return 1
            elif allowed_range[0] >= self.prop_value >= allowed_range[1]:
                return 2
            elif allowed_range[1] >= self.prop_value >= allowed_range[2]:
                return 3
            else:
                return 4
        


    def clean(self):

        if self.prop_value < 0 and self.prop_type != 19:     
            raise ValidationError(f'{self.prop_type} не может быть меньше 0')
       
 

class HazardClassProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    
    CHOICES = (     
        (5, 'Класс опасности в воде'),
        (6, 'Класс опасности в рабочей зоне'),
        (7, 'Класс опасности в атмосферном воздухе'),
        (8, 'Класс опасности в почве'),            
    )

    CLASS_CHOICES = (     
        (1, '1 класс'),
        (2, '2 класс'),
        (3, '3 класс'),
        (4, '4 класс'),            
    )

    prop_type = models.PositiveSmallIntegerField(blank=False, choices=CHOICES)
    prop_value = models.PositiveSmallIntegerField(blank=False, choices=CLASS_CHOICES)
   


class CancerogProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    verbose_name = 'Канцерогенность'
    prop_type = 11
   

    CLASS_CHOICES = (     
        (1, 'Доказана для человека'),
        (2, 'Доказана для животных'),
        (3, 'Есть вероят- ность для животных'),
        (4, 'Неканцероген (доказано)'),            
    )

    
    prop_value = models.PositiveSmallIntegerField(blank=False, choices=CLASS_CHOICES)




class PersistProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    verbose_name = 'Персистентность: трансформация в окружающей среде'
    prop_type = 20
    
    CLASS_CHOICES = (     
        (1, 'Образование болеетоксичных продуктов, в т. ч. обладающих отдаленными эффектами или новыми свойствами'),
        (2, 'Образование продуктов с более выраженным влиянием др. критериев вредности'),
        (3, 'Образование продуктов, токсичность которых близка к токсичности исходного вещества'),
        (4, 'Образование менее токсичных продуктов'),            
    )
    
    prop_value = models.PositiveSmallIntegerField(blank=False, choices=CLASS_CHOICES)

class BioAccProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    verbose_name = 'Биоаккумуляция: поведение в пищевой цепочке'
    prop_type = 21
    
    CLASS_CHOICES = (     
        (1, 'Накопление во всех звеньях'),
        (2, 'Накопление в нескольких звеньях'),
        (3, 'Накопление в одном из звеньев'),
        (4, 'Нет накопления'),            
    )
    
    prop_value = models.PositiveSmallIntegerField(blank=False, choices=CLASS_CHOICES)


class MutagenProp(HazardAbstractProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE)
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE)
    verbose_name = 'Мутагенность'
    prop_type = 22
    
    CLASS_CHOICES = (     
        (1, 'Обнаружена'),
        (2, 'Есть возможность проявления для человека'),
        (3, 'Есть возможность проявления для животных'),
        (4, 'Отсутствует (доказано) '),            
    )
    
    prop_value = models.PositiveSmallIntegerField(blank=False, choices=CLASS_CHOICES)

