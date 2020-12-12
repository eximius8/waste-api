from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import WasteSerializer
from .models import WasteClass, ConcentrationClass
from chemcomponent.models import WasteComponent



@api_view(['POST',])
def calculate_safety_klass_view(request):

    data_in_serializer = WasteSerializer(data=request.data)
    data = []
    if data_in_serializer.is_valid():
        fake_objs = []
        ghost_waste = WasteClass(name=data_in_serializer.validated_data['name'], 
        fkko=data_in_serializer.validated_data['fkko'])        
        for conc in request.data['components']:           
            fake_objs += [ConcentrationClass(waste = ghost_waste,
                                            conc_value = float(conc['concentration'])*1e4,
                                            component = WasteComponent.objects.get(pk=conc['id_val'])),]                                   
            
        # ghost_waste.generate_report(fake_objs, 'test_gcloud_upload')
       
        for concentration in fake_objs:            
            data += [{ "name": concentration.component.name,
                        "concp": float(concentration.conc_value * 1e-4), #"%.2f" % 
                        "concr": concentration.conc_value, 
                        "xi": concentration.component.get_x(), 
                        "zi": concentration.component.get_z(), 
                        "lgw": concentration.component.get_log_w(), 
                        "w": concentration.component.get_w(), 
                        "k": concentration.get_K(),
                        "props": concentration.component.get_props(),
                        "has_x": bool(concentration.component.x_value),
                        "has_soil_c": bool(concentration.component.land_concentration),
                    }]
        return Response({
            "total_k": ghost_waste.get_summ_K(fake_objs=fake_objs),
            "safety_class": ghost_waste.get_safety_class(fake_objs=fake_objs),
            "components": data,
            })
    
    return (Response(data_in_serializer.errors))
            
        

    
""" 
 let components = this.props.components.map((comp) => {
      return { id_val: comp.id, concentrat: parseFloat(comp.concentration) };
    });

 {
    "name": "dsa",
    "fkko": "Хрю хрю",
    "components": [
        {"id_val": 1, "concentrat": 50 },
        {"id_val": 2, "concentrat": 30 },
        {"id_val": 3, "concentrat": 20 }
        ]
}   
     """
    
       
