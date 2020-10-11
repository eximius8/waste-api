from django.contrib import admin

from chemcomponent.models import WasteComponent, HazardValueProp, LiteratureSource

class ChildInline(admin.TabularInline):
    model = HazardValueProp

@admin.register(WasteComponent)
class WasteComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chemical_type', 'W', 'log_W', 'unique_props', 'Binf')
    inlines = [
        ChildInline,
    ]
    
    def W(self, obj):
        return obj.get_w()
    
    def log_W(self, obj):
        return obj.get_log_w()
    
    def unique_props(self, obj):
        return obj.get_num_unique_props()[0]
    
    def Binf(self, obj):
        return obj.get_num_unique_props()[1]




@admin.register(HazardValueProp)
class HazardPropAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'waste_component','literature_source', 'score')
    list_filter = ('waste_component',)

    def name(self, obj):
        return obj.get_prop_type_display()
    
    def value(self, obj):
        return obj.get_val()

    def score(self, obj):
        return obj.get_score()

admin.site.register(LiteratureSource)