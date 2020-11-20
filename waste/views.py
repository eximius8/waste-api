from django.views.generic import DetailView
from rest_framework import viewsets, permissions, filters

from .models import WasteClass
from .serializers import WasteClassSerializer, ConcentrationSerializer

                  

class WasteClassView(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = WasteClassSerializer          
    queryset = WasteClass.objects.all()


class WasteDetailView(DetailView):

    model = WasteClass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        waste = self.get_object()
        waste.generate_report()
        return context