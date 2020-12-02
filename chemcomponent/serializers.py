from rest_framework import serializers
from .models import WasteComponent

from litsource.models import LiteratureSource




class LitSourceSerializer(serializers.ModelSerializer):

    class Meta:

        model = LiteratureSource
        read_only_fields = ('human_name', 'source_url')
        fields =  ('human_name', 'source_url')


class WasteComponentListSerializer(serializers.ModelSerializer):
   

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name', 'other_names')
        fields = ('id', 'name', 'other_names')
        

class WasteComponentSerializer(serializers.ModelSerializer):

    #category_props = CategoryPropSerializer(many=True, read_only=True)
    #value_props = ValuePropSerializer(many=True, read_only=True)
    w_value = serializers.ReadOnlyField(source='get_w')
    lit_source = LitSourceSerializer(read_only=True)

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name', 'w_value', 'chemical_type', 'lit_source', 'category_props', 'value_props', )       
        fields = ('id', 'name', 'w_value', 'chemical_type', 'lit_source', 'category_props', 'value_props',  )