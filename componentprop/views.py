from django.shortcuts import render
from rest_framework import viewsets


from .serializers import CategoryPropSerializer, ValuePropSerializer      
from .models import HazardCategoryProp, HazardValueProp   



class CategoryPropView(viewsets.ModelViewSet):
    
    serializer_class = CategoryPropSerializer          
    queryset = HazardCategoryProp.objects.all()


class ValuePropView(viewsets.ModelViewSet):
    
    serializer_class = ValuePropSerializer          
    queryset = HazardValueProp.objects.all()
