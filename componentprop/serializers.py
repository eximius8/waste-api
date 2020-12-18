from rest_framework import serializers

from componentprop.models import HazardCategoryProp, HazardValueProp#, HazardCategoryType, HazardValueType
from litsource.serializers import LitSourceSerializer


class AbstractPropSerializer(serializers.ModelSerializer):

    def to_representation(self,obj):   

        rep = super(AbstractPropSerializer, self).to_representation(obj)
        literature_source = LitSourceSerializer(obj.literature_source).data
        rep['literature_source'] = [literature_source,]

        return rep

    
    value_type = serializers.StringRelatedField()



class CategoryPropSerializer(AbstractPropSerializer):
   
    score = serializers.IntegerField(source='get_score')
    value = serializers.CharField(source='get_score_str')
    name = serializers.CharField(source='value_type')
    
    
    class Meta:

        model = HazardCategoryProp        
        fields = ('name', 'value', 'score' )



class ValuePropSerializer(AbstractPropSerializer):

    score = serializers.IntegerField(source='get_score')
    value = serializers.CharField(source='prop_float_value')
    name = serializers.CharField(source='value_type')
    
    class Meta:

        model = HazardValueProp       
        fields = ('name', 'value', 'score')
