from rest_framework import serializers


from .models import WasteComponent

class WasteComponentListSerializer(serializers.ModelSerializer):

    #category_props = CategoryPropSerializer(many=True, read_only=True)
    #value_props = ValuePropSerializer(many=True, read_only=True)
    w_value = serializers.ReadOnlyField(source='get_w')

    class Meta:

        model = WasteComponent
        read_only_fields = ('lit_source', 'category_props', 'value_props', )       
        fields = ('id', 'name', 'chemical_type', 'w_value', 'lit_source', 'category_props', 'value_props',  )
        
