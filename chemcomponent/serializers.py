from rest_framework import serializers
from .models import WasteComponent




class WasteComponentListSerializer(serializers.ModelSerializer):
   

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name')
        fields = ('id', 'name')
        

class WasteComponentSerializer(serializers.ModelSerializer):

    #category_props = CategoryPropSerializer(many=True, read_only=True)
    #value_props = ValuePropSerializer(many=True, read_only=True)
    w_value = serializers.ReadOnlyField(source='get_w')

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name', 'other_names', 'w_value')#, 'chemical_type', 'lit_source', 'category_props', 'value_props', )       
        fields = ('id', 'name', 'other_names', 'w_value')#, 'chemical_type', 'lit_source', 'category_props', 'value_props',  )