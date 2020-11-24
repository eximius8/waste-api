from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import WasteSerializer
from .models import WasteClass, ConcentrationClass
from chemcomponent.models import WasteComponent



@api_view(['POST',])
def calculate_safety_klass_view(request):

    data_in_serializer = WasteSerializer(data=request.data)
    if data_in_serializer.is_valid():
        fake_objs = []
        ghost_waste = WasteClass(name=data_in_serializer.validated_data['name'])        
        for conc in request.data['components']:
            fake_objs += [ConcentrationClass(waste=ghost_waste,
                                            conc_value=float(conc['concentrat'])*1e3,
                                            component=WasteComponent.objects.get(pk=conc['id_val'])),]                                   
            
        
        return Response({
            "total_k": ghost_waste.get_summ_K(fake_objs=fake_objs),
            "safet_class": ghost_waste.get_safety_class(fake_objs=fake_objs)})
    
    return (Response(data_in_serializer.errors))
            
        

    
    
    
    
       
