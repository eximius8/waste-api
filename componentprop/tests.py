
from django.test import TestCase

from .models import HazardCategoryType, HazardValueType, HazardValueProp, HazardCategoryProp



class HazardCategoryTypeTests(TestCase):

    def test_value_prop_scores(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        mutagen_type = HazardCategoryType(category1_item="Высокая",
                                            category2_item="Умеренная",
                                            category3_item="Средняя",
                                            category4_item="Низкая")
        pdk_pochva = HazardValueType(bad_val=1.,
                                    average_val=10.,
                                    good_val=100.)

        self.assertEqual(pdk_pochva.get_score(100), 3)
        self.assertEqual(pdk_pochva.get_score(10), 3)
        self.assertEqual(pdk_pochva.get_score(1), 2)       

        self.assertEqual(pdk_pochva.get_score(101), 4)
        self.assertEqual(pdk_pochva.get_score(50), 3)
        self.assertEqual(pdk_pochva.get_score(5), 2)
        self.assertEqual(pdk_pochva.get_score(0.5), 1)

        lg_type = HazardValueType(bad_val=100.,
                                    average_val=50.,
                                    good_val=1.)           
        

        self.assertEqual(lg_type.get_score(101), 1)
        self.assertEqual(lg_type.get_score(100), 2)
        self.assertEqual(lg_type.get_score(50), 3)
        self.assertEqual(lg_type.get_score(1), 3)
        self.assertEqual(lg_type.get_score(75), 2)
        self.assertEqual(lg_type.get_score(25), 3)
        self.assertEqual(lg_type.get_score(0.5), 4)
        
