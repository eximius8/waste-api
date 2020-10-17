from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import WasteComponent
from componentprop.models import HazardCategoryProp, HazardValueProp


class CategoryPropSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = HazardCategoryProp
        fields = ('id', 'value_type', 'prop_category_value', 'literature_source')

class ValuePropSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = HazardValueProp
        fields = ('id', 'value_type', 'prop_float_value', 'literature_source')

class WasteComponentSerializer(serializers.ModelSerializer):

    category_props = CategoryPropSerializer(many=True, read_only=True)
    value_props = ValuePropSerializer(many=True, read_only=True)
    w_value = serializers.ReadOnlyField(source='get_w')

    class Meta:

        model = WasteComponent
        read_only_fields = ('lit_source', )       
        fields = ('id', 'name', 'chemical_type', 'w_value', 'lit_source', 'category_props', 'value_props',  )
        

        # validators = [
        #                 UniqueTogetherValidator(
        #                     queryset=WasteComponent.objects.all(),
        #                     fields=['list', 'position']
        #                 )
        #             ]