from django.contrib import admin

from chemcomponent.models import WasteComponent
from componentprop.models import HazardValueProp, HazardCategoryProp


class ValuePropInline(admin.TabularInline):
    model = HazardValueProp

class CategoryPropInline(admin.TabularInline):
    model = HazardCategoryProp

@admin.register(WasteComponent)
class WasteComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chemical_type', 'W', 'log_W', 'unique_props', 'Binf')
    inlines = [
        ValuePropInline,
        CategoryPropInline,
    ]
    
    def W(self, obj):
        return obj.get_w()
    
    def log_W(self, obj):
        return obj.get_log_w()
    
    def unique_props(self, obj):
        return obj.get_num_unique_props()[0]
    
    def Binf(self, obj):
        return obj.get_num_unique_props()[1]






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
    

   

