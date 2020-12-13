from django.contrib import admin
from django.db import models
from django.forms import TextInput

from chemcomponent.models import WasteComponent
from componentprop.models import HazardValueProp, HazardCategoryProp#, HazardComplexValueProp


class ValuePropInline(admin.TabularInline):
    model = HazardValueProp

#class ComplexValuePropInline(admin.TabularInline):
 #   model = HazardComplexValueProp

class CategoryPropInline(admin.TabularInline):
    model = HazardCategoryProp

@admin.register(WasteComponent)
class WasteComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chemical_type', 'X', 'Z', 'log_W', 'W', 'number_of_props')#, 'Binf')
    search_fields = ['name', 'other_names', 'cas_number']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},        
    }
    inlines = [
        ValuePropInline,
       # ComplexValuePropInline,
        CategoryPropInline,
    ]

    def X(self, obj):
        return round(obj.get_x(), 3)
    
    def Z(self, obj):
        return round(obj.get_z(), 3)

    def log_W(self, obj):
        return round(obj.get_log_w(), 3)
    
    def W(self, obj):
        return round(obj.get_w(), 2)
    
    
    
    def number_of_props(self, obj):
        return len(obj.get_props())
    
"""     def Binf(self, obj):
        return obj.get_num_unique_props()[1] """






# # @admin.register(HazardValueProp)
# # class HazardPropAdmin(admin.ModelAdmin):
# #     list_display = ('waste_component', 'value_type', 'prop_float_value', 'score', 'literature_source')

# #     def score(self, obj):
# #         return obj.get_score()

# # @admin.register(HazardClassProp)
# # class HazardPropAdmin(admin.ModelAdmin):
# #     list_display = ('waste_component', 'value_type',  'score', 'literature_source')

# #     def score(self, obj):
# #         return obj.get_score()
    

   

