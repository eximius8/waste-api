from django.shortcuts import render
from rest_framework import viewsets


from .serializers import WasteComponent      
from .models import WasteComponent                   

class ComponenterView(viewsets.ModelViewSet):
    
    serializer_class = WasteComponent          
    queryset = WasteComponent.objects.all()

    