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
    concentration = serializers.FloatField(min_value=0., max_value=100.)

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
    fkko = serializers.CharField(max_length=30)

    def validate_components(self, comps):        
        sum_conc = 0
        for component in comps:
            sum_conc += float(component['concentration'])
        if sum_conc > 100:
            raise serializers.ValidationError("Сумма всех концентраций не может быть больше 100!")


    
