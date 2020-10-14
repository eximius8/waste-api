from django.views.generic import DetailView

from .models import WasteClass

class WasteDetailView(DetailView):

    model = WasteClass

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        waste = self.get_object()
        waste.generate_report()
        return context