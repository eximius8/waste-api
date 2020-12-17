from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import WasteComponent
from .views import comp_statistics
from componentprop.models import HazardCategoryType, HazardValueType, HazardValueProp, HazardCategoryProp
from litsource.models import LiteratureSource


class WasteComponentTests(TestCase):

    def test_run(self):

        self.for_models()
        self.for_api()
        self.create_comp_with_lg_prop()

    def test_simple(self):

        self.setup()
        self.water = WasteComponent.objects.create(name="water",
                                                    x_value_lit_source=self.gost_src,
                                                    x_value=4)
        self.assertEqual(self.water.get_z(), 5) 
        self.assertEqual(self.water.get_log_w(), 6)         
        self.assertEqual(self.water.get_w(), 1e6) 



        self.aldrin = WasteComponent.objects.create(name="Альдрин",
                                                    x_value_lit_source=self.gost_src,
                                                    x_value=1.855)
        self.assertAlmostEqual(self.aldrin.get_z(), 2.14, places=1) 
        self.assertAlmostEqual(self.aldrin.get_log_w(), 2.14, places=1)         
        self.assertAlmostEqual(self.aldrin.get_w(), 138, places=0) 

        self.benzpiren = WasteComponent.objects.create(name="benzpiren",
                                                     x_value_lit_source=self.gost_src,
                                                     x_value=1.6)
        self.assertAlmostEqual(self.benzpiren.get_z(), 1.8, places=4) 
        self.assertAlmostEqual(self.benzpiren.get_log_w(), 1.778, places=3)         
        self.assertAlmostEqual(self.benzpiren.get_w(), 59.97, places=1) 


    def for_models(self):
        self.setup()
        self.create_waste_component_numbers_with_1_cat_prop()
        self.create_waste_component_with_1_num_prop()
        self.create_waste_component_numbers_with_many_props()

    def for_api(self):
        
        factory = APIRequestFactory()
        request = factory.get('/components/total/')        
        response = comp_statistics(request)

        self.assertEqual(response.data['totalcomps'], 3)


    def setup(self):
        """
        creating auxilary objects
        """
        self.klass_op_soil_type = HazardCategoryType.objects.create(category1_item="1",
                                                                    category2_item="2",
                                                                    category3_item="3",
                                                                    category4_item="Не установлен")

        self.klass_op_xoz_voda = HazardCategoryType.objects.create(category1_item="1",
                                                                    category2_item="2",
                                                                    category3_item="3",
                                                                    category4_item="4")

        self.klass_op_fish_water = HazardCategoryType.objects.create(category1_item="1",
                                                                    category2_item="2",
                                                                    category3_item="3",
                                                                    category4_item="4")

        self.klass_op_air = HazardCategoryType.objects.create(category1_item="1",
                                                                    category2_item="2",
                                                                    category3_item="3",
                                                                    category4_item="4")

        self.pdk_pochva = HazardValueType.objects.create(bad_val=1.,
                                                        average_val=10.,
                                                        good_val=100.)
        self.pdk_ss = HazardValueType.objects.create(bad_val=.01,
                                                     average_val=.1,
                                                     good_val=1.)

        self.pdk_voda = HazardValueType.objects.create(bad_val=.001,
                                                     average_val=.01,
                                                     good_val=1.)
                                                    
        self.pdk_r_h = HazardValueType.objects.create(bad_val=.001,
                                                     average_val=.01,
                                                     good_val=0.1)
        self.lg_kow = HazardValueType.objects.create(bad_val=4,
                                                     average_val=2,
                                                     good_val=0)
      
        self.gost_src = LiteratureSource.objects.create(name="Gost", latexpart="Bred")

    def create_waste_component_numbers_with_many_props(self):
        """
        http://eco-profi.info/download_instr/47110101521_lamp.pdf
        """
        
        self.porcelain = WasteComponent.objects.create(name="Фарфор")
        self.porcelain_pdk_v = HazardValueProp.objects.create(waste_component=self.porcelain,
                                                              value_type=self.pdk_voda,
                                                              prop_float_value=0.25,
                                                              literature_source=self.gost_src)

        
        self.porcelain_klass_op_xoz_voda = HazardCategoryProp.objects.create(waste_component=self.porcelain,
                                                                            value_type=self.klass_op_xoz_voda,
                                                                            prop_category_value=4,
                                                                            literature_source=self.gost_src)

        self.porcelain_pdk_r_h = HazardValueProp.objects.create(waste_component=self.porcelain,
                                                                value_type=self.pdk_r_h,
                                                                prop_float_value=0.5,
                                                                literature_source=self.gost_src)

        
        self.porcelain_klass_op_fish_vod = HazardCategoryProp.objects.create(waste_component=self.porcelain,
                                                                            value_type=self.klass_op_fish_water,
                                                                            prop_category_value=4,
                                                                            literature_source=self.gost_src)

        self.porcelain_pdk_ss = HazardValueProp.objects.create(waste_component=self.porcelain,
                                                              value_type=self.pdk_ss,
                                                              prop_float_value=0.03,
                                                              literature_source=self.gost_src)

        
        self.porcelain_klass_op_air = HazardCategoryProp.objects.create(waste_component=self.porcelain,
                                                                            value_type=self.klass_op_air,
                                                                            prop_category_value=2,
                                                                            literature_source=self.gost_src)                                                                                                                                    

        self.assertEqual(self.porcelain.get_x(), 3.)
        self.assertAlmostEqual(self.porcelain.get_z(), 3.67, places=2)
        self.assertAlmostEqual(self.porcelain.get_log_w(), 3.67, places=2)
        self.assertAlmostEqual(self.porcelain.get_k(4500), 0.969, places=1)
        self.assertAlmostEqual(self.porcelain.get_w(), 4641.588, places=2) 

    
    def create_waste_component_numbers_with_1_cat_prop(self):
        """
        http://eco-profi.info/download_instr/47110101521_lamp.pdf
        """
        
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

    

    def create_waste_component_with_1_num_prop(self):
        """
        http://eco-profi.info/download_instr/47110101521_lamp.pdf
        """
                               
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

    
    def create_comp_with_lg_prop(self):

        self.orgnic_shit = WasteComponent.objects.create(name="Органика")
        self.orgnic_shit_lg_kow = HazardValueProp.objects.create(waste_component=self.orgnic_shit,
                                                                value_type=self.lg_kow,
                                                                prop_float_value=5,
                                                                literature_source=self.gost_src)

        self.assertEqual(self.orgnic_shit.get_x(), 1)
        self.assertEqual(self.orgnic_shit.Binf()[1], 1)

        self.orgnic_shit2 = WasteComponent.objects.create(name="Органика")
        self.orgnic_shit2_lg_kow = HazardValueProp.objects.create(waste_component=self.orgnic_shit2,
                                                                value_type=self.lg_kow,
                                                                prop_float_value=3,
                                                                literature_source=self.gost_src)

        self.assertEqual(self.orgnic_shit2.get_x(), 1.5)
       
    

        
        
