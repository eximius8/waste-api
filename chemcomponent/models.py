from django.db import models

from django.core.exceptions import ValidationError

class LiteratureSource(models.Model):

    name = models.CharField(blank=False, max_length=100, unique=True)
    latexpart = models.TextField(blank=False)

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Литературный источник"
        verbose_name_plural = "Литературные источники"



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
        get number of hazard_props with unique importances
        should be updated to distinct
        """
        x = set()
        for prop in self.class_props.all():
            x.add(prop.importance)
        for prop in self.value_props.all():
            x.add(prop.importance)        
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
        for value_prop in self.value_props.all():
            if not value_prop.importance in x:                
                x.add(value_prop.importance)
                BigX += value_prop.get_score()
        for class_prop in self.class_props.all():
            if not class_prop.importance in x:                
                x.add(class_prop.importance)
                BigX += class_prop.get_score()

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
        if self.good_val < self.bad_val:
            if obj_value < self.good_val:
                return 4
            elif obj_value > self.bad_val:
                return 1
            elif self.good_val <= obj_value <= self.average_val:
                return 3
            elif self.average_val < obj_value <= self.bad_val:
                return 2

        if obj_value > self.good_val:
            return 4
        elif obj_value < self.bad_val:
            return 1
        elif self.average_val <= obj_value <= self.good_val:
            return 3
        elif self.bad_val < obj_value <= self.average_val:
            return 2


    def clean(self):
        if self.good_val < self.bad_val and (self.average_val < self.good_val or self.average_val > self.bad_val):
            raise ValidationError(f'Среднее значение должно быть между {self.good_val} и {self.bad_val}')
        
        if self.bad_val < self.good_val and (self.average_val < self.bad_val or self.average_val > self.good_val):
            raise ValidationError(f'Среднее значение должно быть между {self.bad_val} и {self.good_val}')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Числовой параметр"
        verbose_name_plural = "Числовые параметры"
   

class AbstractHazardProp(models.Model):
    
    importance = models.PositiveSmallIntegerField(blank=False,                                                 
                                                 verbose_name='Важность')

    class Meta:
        abstract = True

class HazardValueProp(AbstractHazardProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE, related_name='value_props')
    

    value_type = models.ForeignKey(HazardValueType, on_delete=models.CASCADE, related_name='valprops')
    prop_float_value = models.FloatField(blank=False, 
                                         null=False,
                                         verbose_name='Числовое значение')
    literature_source = models.ForeignKey(LiteratureSource, on_delete=models.CASCADE, related_name='value_props')

    def get_score(self):

        return self.value_type.get_score(self.prop_float_value)

    def __str__(self):
        return f'{self.value_type} - диапазон значений от плохого к хорошему: {self.value_type.bad_val} - {self.value_type.average_val} - {self.value_type.good_val}'

    
    class Meta:
        verbose_name = "Числовое свойство"
        verbose_name_plural = "Числовые свойства"

class HazardClassType(models.Model):

    name = models.CharField(max_length=400, blank=False, verbose_name="Название")

    class1_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 1")
    class2_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 2")
    class3_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 3")
    class4_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 4")

    def __str__(self):
        return self.name

class HazardClassProp(AbstractHazardProp):

    waste_component = models.ForeignKey(WasteComponent, on_delete=models.CASCADE, related_name='class_props')
    

    value_type = models.ForeignKey(HazardClassType, on_delete=models.CASCADE, related_name='classprops')
    prop_class_value = models.PositiveSmallIntegerField(blank=False, 
                                                 null=False,                                                       
                                                 verbose_name='Класс опасности')
    literature_source = models.ForeignKey(LiteratureSource, 
                                          on_delete=models.CASCADE, 
                                          related_name='class_props',
                                          verbose_name='Литература')

    def __str__(self):
        return \
        f'{self.value_type} - возможные значения 1- {self.value_type.class1_item}, 2 - {self.value_type.class2_item},\
         3 - {self.value_type.class3_item}, 4 - {self.value_type.class4_item}'


    def get_score(self):

        return self.prop_class_value

   