from rest_framework import serializers
from waste.models import WasteClass, ConcentrationClass

from chemcomponent.models import WasteComponent



def component_exists(value):
    try:
        WasteComponent.objects.get(pk=value)
    except WasteComponent.DoesNotExist:
        raise serializers.ValidationError('Не найдено')

class CommponSerializer(serializers.Serializer):
    
    id_val = serializers.IntegerField(min_value=0, validators=[component_exists,])
    concentrat = serializers.FloatField(min_value=0., max_value=100.)

""" {
"name": "New waste",
"components": [
{"id_val": "17", "concentrat": "1"},
{"id_val": "19", "concentrat": "1"},
{"id_val": "16", "concentrat": "100"}
]
} """


class WasteSerializer(serializers.Serializer):
    components = CommponSerializer(required=True, many=True)
    name = serializers.CharField(max_length=200)
    
