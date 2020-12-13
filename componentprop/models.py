from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator 

class AbstractHazardPropType(models.Model):
    """
    Тип свойства это такие вещи как ПДК, мутагенность и т.д.
    индивидуальны для каждого компонента
    """   
  
    name = models.CharField(max_length=400, blank=False, verbose_name="Название")
    short_name = models.CharField(max_length=100, blank=False, default="", verbose_name="Короткое название")

    def __str__(self):
        return self.short_name

    class Meta:
        abstract = True

class HazardCategoryType(AbstractHazardPropType):    

    category1_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 1")
    category2_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 2")
    category3_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 3")
    category4_item = models.CharField(max_length=100, blank=False, verbose_name="Свойство класса 4")

    def get_score(self, obj_value):
        valu = eval(f"self.category{str(obj_value)}_item")
        return valu

    class Meta:
        verbose_name = "Категория классификации"
        verbose_name_plural = "Категории классификации"


class HazardCategoryProp(models.Model):

    waste_component = models.ForeignKey('chemcomponent.WasteComponent', on_delete=models.CASCADE, related_name='category_props')   

    value_type = models.ForeignKey(HazardCategoryType, on_delete=models.CASCADE, related_name='category_props')
    prop_category_value = models.PositiveSmallIntegerField(blank=False, 
                                                            validators=[MaxValueValidator(4),MinValueValidator(1)],
                                                            null=False,                                                       
                                                            verbose_name='Класс опасности')
    literature_source = models.ForeignKey('litsource.LiteratureSource', 
                                          on_delete=models.CASCADE, 
                                          related_name='category_props',
                                          verbose_name='Литература')

    def __str__(self):
        return \
        f'{self.value_type} - возможные значения 1 - {self.value_type.category1_item}, 2 - {self.value_type.category2_item},\
         3 - {self.value_type.category3_item}, 4 - {self.value_type.category4_item}'
    
    def get_json(self):
        json_prop_data = {}
        json_prop_data['name'] = self.value_type.short_name        
        string = f"self.value_type.category{self.prop_category_value}_item"       
        
        json_prop_data['data'] = {
                            'litsource': self.literature_source.name,
                            'value': eval(string),
                            'score': self.get_score()  
                            }           

        return json_prop_data

    def get_score_str(self):

        return self.value_type.get_score(self.prop_category_value)


    def get_score(self):

        return self.prop_category_value

    class Meta:

        unique_together = ['waste_component', 'value_type']
        verbose_name = "Свойство классификации"
        verbose_name_plural = "Свойства классификации"



class HazardValueType(AbstractHazardPropType):    

    bad_val = models.FloatField(blank=False, verbose_name="Значение больше или меньше которого класс опасности = 1")
    average_val = models.FloatField(blank=False, verbose_name="Среднее значение")
    good_val = models.FloatField(blank=False, verbose_name="Значение больше или меньше которого класс опасности = 4")

    def get_score(self, obj_value):
        
        if self.good_val < self.bad_val:
            if obj_value < self.good_val:
                return 4
            elif self.good_val <= obj_value <= self.average_val:
                return 3
            elif self.average_val < obj_value <= self.bad_val:
                return 2
            elif obj_value > self.bad_val:
                return 1            
            

        if obj_value > self.good_val:
            return 4
        elif self.average_val <= obj_value <= self.good_val:
            return 3
        elif self.bad_val <= obj_value < self.average_val:
            return 2
        elif obj_value < self.bad_val:
            return 1


    def clean(self):
        if self.good_val < self.bad_val and (self.average_val < self.good_val or self.average_val > self.bad_val):
            raise ValidationError(f'Среднее значение должно быть между {self.good_val} и {self.bad_val}')
        
        if self.bad_val < self.good_val and (self.average_val < self.bad_val or self.average_val > self.good_val):
            raise ValidationError(f'Среднее значение должно быть между {self.bad_val} и {self.good_val}')
   

    class Meta:
        verbose_name = "Числовой параметр"
        verbose_name_plural = "Числовые параметры"
   

class HazardValueProp(models.Model):
    """
    Само свойство (числовое значение или категория) - относится как компоненту отхода так и имеет тип (ПДК мутагенность и т.п.)
    """

    waste_component = models.ForeignKey('chemcomponent.WasteComponent', on_delete=models.CASCADE, related_name='value_props')
    value_type = models.ForeignKey(HazardValueType, on_delete=models.CASCADE, related_name='value_props')
    prop_float_value = models.FloatField(blank=False, 
                                         null=False,
                                        # validators=[MinValueValidator(0.),],
                                         verbose_name='Числовое значение')
    literature_source = models.ForeignKey('litsource.LiteratureSource', 
                                          on_delete=models.CASCADE, 
                                          related_name='value_props', 
                                          verbose_name='Литература')

    def get_json(self):
        json_prop_data = {}
        json_prop_data['name'] = self.value_type.short_name
        json_prop_data['data'] = {
                            'litsource': self.literature_source.name,
                            'value': self.prop_float_value,
                            'score': self.get_score()  
                            }      

        return json_prop_data


    def get_score(self):      
        

        return self.value_type.get_score(self.prop_float_value)

    def __str__(self):
        return f'{self.value_type} - диапазон значений от плохого к хорошему: \
         {self.value_type.bad_val} - {self.value_type.average_val} - {self.value_type.good_val}'

    
    class Meta:

        unique_together = ['waste_component', 'value_type']
        verbose_name = "Числовое свойство"
        verbose_name_plural = "Числовые свойства"    
  


class ValueProp(models.Model):
    """
    Props для составных свойств
    Lg (S, мг/л / ПДКв, мг.л) 
    """
    waste_component = models.ForeignKey('chemcomponent.WasteComponent', on_delete=models.CASCADE, related_name='value_complex_props')
    value_type = models.ForeignKey(HazardValueType, on_delete=models.CASCADE, related_name='value_complex_props')
    prop_float_value = models.FloatField(blank=False, 
                                         null=False,
                                         validators=[MinValueValidator(0.),],
                                         verbose_name='Числовое значение')
    literature_source = models.ForeignKey('litsource.LiteratureSource', 
                                          on_delete=models.CASCADE, 
                                          related_name='value_complex_props', 
                                          verbose_name='Литература')

    class Meta:

        unique_together = ['waste_component', 'value_type']
        verbose_name = "Числовое свойство для комплексных вычислений типа Lg (S, мг/л / ПДКв, мг.л)"
        verbose_name_plural = "Числовые свойства для комплексных вычислений типа Lg (S, мг/л / ПДКв, мг.л)"                                    

