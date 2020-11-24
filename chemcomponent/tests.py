from django.test import TestCase

from .models import WasteComponent
from componentprop.models import HazardCategoryType, HazardValueType, HazardValueProp, HazardCategoryProp
from litsource.models import LiteratureSource


class WasteComponentTests(TestCase):

    def setup(self):
        """
        creating auxilary objects
        """
        self.klass_op_soil_type = HazardCategoryType.objects.create(category1_item="1",
                                                                    category2_item="2",
                                                                    category3_item="3",
                                                                    category4_item="Не установлен")
        self.pdk_pochva = HazardValueType.objects.create(bad_val=1.,
                                                        average_val=10.,
                                                        good_val=100.)
        self.pdk_ss = HazardValueType.objects.create(bad_val=.01,
                                                     average_val=.1,
                                                     good_val=1.)

      
        self.gost_src = LiteratureSource.objects.create(name="Gost", latexpart="Bred")
    
    def test_waste_component_numbers_with_1_cat_prop(self):
        """
        http://eco-profi.info/download_instr/47110101521_lamp.pdf
        """
        self.setup()
        self.latun = WasteComponent.objects.create(name="Латунь")
        self.latun_klass_op_soil = HazardCategoryProp.objects.create(waste_component=self.latun,
                                                                    value_type=self.klass_op_soil_type,
                                                                    prop_category_value=1,
                                                                    literature_source=self.gost_src)

        self.assertEqual(self.latun.get_x(), 1.)
        self.assertAlmostEqual(self.latun.get_z(), 1., places=2)
        self.assertEqual(self.latun.get_log_w(), 0)
        self.assertAlmostEqual(self.latun.get_k(80800), 80800, places=1)
        self.assertAlmostEqual(self.latun.get_w(), 1, places=2) 

    

    def test_waste_component_with_1_num_prop(self):
        """
        http://eco-profi.info/download_instr/47110101521_lamp.pdf
        """
        self.setup()
                       
        self.mastika = WasteComponent.objects.create(name="Мастика")
        self.mastika_pdk_ss = HazardValueProp.objects.create(waste_component=self.mastika,
                                                            value_type=self.pdk_ss,
                                                            prop_float_value=0.01,
                                                            literature_source=self.gost_src)        
        
        self.assertEqual(self.mastika.get_x(), 1.5)
        self.assertAlmostEqual(self.mastika.get_z(), 1.67, places=2)
        self.assertEqual(self.mastika.get_log_w(), 1.6)
        self.assertAlmostEqual(self.mastika.get_k(18200), 457.2, places=1)
        self.assertAlmostEqual(self.mastika.get_w(), 39.81, places=2)

    

        
        
