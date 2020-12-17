from rest_framework import serializers
from .models import WasteComponent

from componentprop.serializers import CategoryPropSerializer, ValuePropSerializer
from litsource.serializers import LitSourceSerializer


class WasteComponentListSerializer(serializers.ModelSerializer):
   

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name', 'other_names')
        fields = ('id', 'name', 'other_names')
        

class WasteComponentSerializer(serializers.ModelSerializer):
   
    w_value = serializers.ReadOnlyField(source='get_w')
    #lit_source = LitSourceSerializer(read_only=True)
    category_props = CategoryPropSerializer(many=True, read_only=True)
    value_props = ValuePropSerializer(many=True, read_only=True)

    class Meta:

        model = WasteComponent
        #read_only_fields = ('id', 'name', 'w_value', 'chemical_type', 'lit_source', 'category_props', 'value_props', 'Binf')       
        fields = ('id', 'name', 'w_value', 'chemical_type', ('xpk', 'xpk_lit_source',), 'category_props', 'value_props',  'Binf')