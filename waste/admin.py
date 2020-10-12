from django.contrib import admin

from waste.models import WasteClass, Concentration
from chemcomponent.models import WasteComponent



class WasteComponentInline(admin.TabularInline):
    model = Concentration



@admin.register(WasteClass)
class WasteClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'K_val', 'safety_klass')
    inlines = [
        WasteComponentInline,        
    ]

    def safety_klass(self, obj):
        return obj.get_safety_class()
    
    def K_val(self, obj):
        return obj.get_summ_K()    


