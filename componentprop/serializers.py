from rest_framework import serializers

from componentprop.models import HazardCategoryProp, HazardValueProp


class CategoryPropSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = HazardCategoryProp
        fields = ('id', 'waste_component', 'value_type', 'prop_category_value', 'literature_source', )

class ValuePropSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = HazardValueProp
        fields = ('id', 'waste_component', 'value_type', 'prop_float_value', 'literature_source',)
