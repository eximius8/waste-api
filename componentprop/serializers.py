from rest_framework import serializers

from componentprop.models import HazardCategoryProp, HazardValueProp#, HazardCategoryType, HazardValueType
from litsource.serializers import LitSourceSerializer


class AbstractPropSerializer(serializers.ModelSerializer):

    literature_source = LitSourceSerializer(read_only=True)
    value_type = serializers.StringRelatedField()



class CategoryPropSerializer(AbstractPropSerializer):
    
    class Meta:

        model = HazardCategoryProp
        read_only_fields = ('value_type', 'get_score_str', 'literature_source', 'get_score' )
        fields = ('value_type', 'get_score_str', 'literature_source', 'get_score' )



class ValuePropSerializer(AbstractPropSerializer):

    
    class Meta:

        model = HazardValueProp
        read_only_fields = ('value_type', 'prop_float_value', 'literature_source', 'get_score')
        fields = ('value_type', 'prop_float_value', 'literature_source', 'get_score')
