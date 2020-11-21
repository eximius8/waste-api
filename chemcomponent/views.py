from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.filters import SearchFilter, OrderingFilter
#from django_filters.rest_framework import DjangoFilterBackend


from .serializers import WasteComponentListSerializer, WasteComponentSerializer   
from .models import WasteComponent   


class ComponentsView(generics.ListAPIView):
    queryset =  WasteComponent.objects.all()
    serializer_class = WasteComponentListSerializer
   
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'other_names']
    ordering_fields = ['name',]


class ComponentView(generics.RetrieveAPIView):

    queryset =  WasteComponent.objects.all()    
    serializer_class = WasteComponentSerializer
   