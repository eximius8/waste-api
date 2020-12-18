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

    
    
    class Meta:

        model = HazardCategoryProp        
        fields = ('value_type', 'get_score_str', 'get_score' )



class ValuePropSerializer(AbstractPropSerializer):
    
    class Meta:

        model = HazardValueProp       
        fields = ('value_type', 'prop_float_value', 'get_score')
