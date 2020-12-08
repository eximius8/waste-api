from litsource.models import LiteratureSource
from componentprop.models import HazardCategoryType, HazardValueType
from chemcomponent.models import WasteComponent
import csv




prikaz = LiteratureSource.objects.create(name="prikadzfdIIV",
                          source_type = "prikaz", latexpart = "das",
                          human_name = "Приказ минприр 536")


soil_safety_class = HazardCategoryType.objects.create(name="Класс опасности в почве",
                                                      short_name="Класс опасности в почве",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="Не установлен")

drink_water_safety_class = HazardCategoryType.objects.create(
    name="Класс опасности в воде водных объектов, используемых для целей питьевого и хозяйственно-бытового водоснабжения",
                                                      short_name="Класс опасности в питьевой воде",
                                                      category1_item="1",
                                                      category2_item="2",
                                                      category3_item="3",
                                                      category4_item="4")


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


with open('mpr536.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[2]:
            WasteComponent.objects.create(name=row[0],
                                          x_value=float(row[1]),
                                          lit_source=prikaz,
                                          cas_number=row[2])
        else:
            WasteComponent.objects.create(name=row[0],
                                          lit_source=prikaz,
                                          x_value=float(row[1]))                                          
    