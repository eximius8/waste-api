from django.shortcuts import render
from rest_framework import viewsets


from .serializers import WasteComponentSerializer      
from .models import WasteComponent                   

class ComponenterView(viewsets.ModelViewSet):
    
    serializer_class = WasteComponentSerializer          
    queryset = WasteComponent.objects.all()

    