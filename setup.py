from litsource.models import LiteratureSource
from componentprop.models import HazardCategoryType, HazardValueType
from chemcomponent.models import WasteComponent
import csv

# python ./manage.py shell < setup.py


prikaz = LiteratureSource.objects.create(name="prikazIIV",
                          source_type = "prikaz", latexpart = "das",
                          human_name = "Приказ минприр 536")


soil_safety_class = HazardCategoryType.objects.create(name="Класс опасности в почве",
                                                      short_name="Класс опасности в почве",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="Не установлен")

""" 
drink_water_safety_class = HazardCategoryType.objects.create(
    name="Класс опасности в воде водных объектов, используемых для целей питьевого и хозяйственно-бытового водоснабжения",
                                                      short_name="Класс опасности в питьевой воде",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="4") """


fish_water_safety_class = HazardCategoryType.objects.create(
    name="Класс опасности в воде водных объектов рыбохозяйственного значения",
                                                      short_name="Класс опасности в воде рыбохозяйственного значения",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="4")
                                                    

air_safety_class = HazardCategoryType.objects.create(
                                                      name="Класс опасности в атмосферном воздухе",
                                                      short_name="Класс опасности в воздухе",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="4")


presistance_safety_class = HazardCategoryType.objects.create(
                                                      name="Персистентность (трансформация в окружающей среде)",
                                                      short_name="Персистентность",
                                                      category1_item="Образование более токсичных продуктов, в т.ч. обладающих отдаленными эффектами или новыми свойствами",
                                                      category2_item="Образование продуктов с более выраженным влиянием других критериев опасности",
                                                      category3_item="Образование продуктов, токсичность которых близка к токсичности исходного вещества",
                                                      category4_item="Образование менее токсичных продуктов")


bioacc = HazardCategoryType.objects.create(
                                            name="Биоаккумуляция (поведение в пищевой цепочке)",
                                            short_name="Биоаккумуляция",
                                            category1_item="Выраженное накопление во всех звеньях",
                                            category2_item="Накопление в нескольких звеньях",
                                            category3_item="Накопление в одном из звеньев",
                                            category4_item="Накопление отсутствует")

pdk_pochva = HazardValueType.objects.create(name="Предельно допустимая концентрация вещества в почве",
                                            short_name="ПДКп, мг/кг",bad_val=1, average_val=10, good_val=100)


pdk_drink_water = HazardValueType.objects.create(
    name="Предельно допустимая концентрация вещества в воде водных объектов, используемых для целей питьевого и хозяйственно-бытового водоснабжения",
                                            short_name="ПДКв, мг/л",bad_val=0.01, average_val=0.1, good_val=1)

pdk_fish_water = HazardValueType.objects.create(
    name="Предельно допустимая концентрация вещества в воде водных объектов рыбохозяйственного значения",
                                            short_name="ПДКрх, мг/л",bad_val=0.001, average_val=0.01, good_val=0.1)


pdk_ss = HazardValueType.objects.create(
    name="Предельно допустимая концентрация вещества среднесуточная в атмосферном воздухе населенных мест",
                                            short_name="ПДКсс, мг/м^3",bad_val=0.01, average_val=0.1, good_val=1)                                        


pdk_pp = HazardValueType.objects.create(
    name="Предельно допустимая концентрация вещества в пищевых продуктах",
                                            short_name="ПДКпп, мг/кг",bad_val=0.01, average_val=1, good_val=10)


ld_50 = HazardValueType.objects.create(
    name="Средняя смертельная доза компонента в миллиграммах действующего вещества на 1 кг живого веса, вызывающая гибель 50% подопытных животных при однократном пероральном введении в унифицированных условиях",
                                            short_name="LD50, мг/кг", bad_val=15, average_val=150, good_val=5000)  

lc_50 = HazardValueType.objects.create(
    name="Средняя смертельная концентрация вещества, вызывающая гибель 50% подопытных животных при ингаляционном поступлении в унифицированных условиях",
                                            short_name="LC50, мг/м3",bad_val=500, average_val=5000, good_val=50000)  

lc_50_water = HazardValueType.objects.create(
    name="Средняя смертельная концентрация вещества в воде, вызывающая гибель 50% всех взятых в опыт гидробионтов (например, рыб) через 96 часов",
                                            short_name="LC50 водн, мг/л/96 ч",bad_val=1, average_val=5, good_val=100) 

with open('mpr536.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[2]:
            WasteComponent.objects.create(name=row[0],
                                          x_value=float(row[1]),
                                          x_value_lit_source=prikaz,
                                          cas_number=row[2])
        else:
            WasteComponent.objects.create(name=row[0],
                                          x_value_lit_source=prikaz,
                                          x_value=float(row[1]))                                          
    