from rest_framework import serializers
from waste.models import WasteClass, Concentration




class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

class ConcentrationSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Concentration
        fields = ('component__pk', 'conc_value')



class WasteClassSerializer(serializers.ModelSerializer):


    concentrat = ConcentrationSerializer()
    
    class Meta:

        model = WasteClass
        fields = ( 'name',  'concentrat')
