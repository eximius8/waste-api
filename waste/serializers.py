from rest_framework import serializers

from waste.models import WasteClass, Concentration


class WasteClassSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = WasteClass
        fields = ('id', 'name', 'fkko',  )

class ConcentrationSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Concentration
        fields = ('id', 'waste',)
