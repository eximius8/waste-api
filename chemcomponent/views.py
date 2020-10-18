from django.shortcuts import render
from rest_framework import viewsets, permissions, filters


from .serializers import WasteComponentListSerializer      
from .models import WasteComponent                   

class ComponenterView(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = WasteComponentListSerializer          
    queryset = WasteComponent.objects.all()

    