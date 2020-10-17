from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import WasteComponent
from componentprop.models import HazardCategoryProp


class CategoryPropSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = HazardCategoryProp
        fields = ('id', 'value_type', 'prop_category_value', 'literature_source')

class WasteComponentSerializer(serializers.ModelSerializer):

    category_props = CategoryPropSerializer(many=True, read_only=True)

    class Meta:

        model = WasteComponent
        fields = ('id', 'name', 'chemical_type', 'category_props')

        # validators = [
        #                 UniqueTogetherValidator(
        #                     queryset=WasteComponent.objects.all(),
        #                     fields=['list', 'position']
        #                 )
        #             ]