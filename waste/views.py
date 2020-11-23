from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import WasteClassSerializer



@api_view(['POST',])
def calculate_safety_klass_view(request):

    newobj = WasteClassSerializer(request.data)
    print(newobj)
    
    return Response({"message": "Got some data!", "data": request.data})
    
       
