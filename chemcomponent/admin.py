from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django import forms

from chemcomponent.models import WasteComponent
from componentprop.models import HazardValueProp, HazardCategoryProp#, HazardComplexValueProp


class ValuePropInline(admin.TabularInline):
    model = HazardValueProp

class WasteComponentAdminForm(forms.ModelForm):
	cas_number = forms.CharField(widget=forms.TextInput(attrs={'size':50}), required=False)

class CategoryPropInline(admin.TabularInline):
    model = HazardCategoryProp

@admin.register(WasteComponent)
class WasteComponentAdmin(admin.ModelAdmin):
    form = WasteComponentAdminForm
    list_display = ('name', 'chemical_type', 'X', 'Z', 'log_W', 'W', 'number_of_props', 'B_inf')
    search_fields = ['name', 'other_names', 'cas_number']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},        
    }
    fields = (
        'name',
        'other_names',
        ('chemical_type', 'cas_number',),
        ('x_value', 'x_value_lit_source'),
        ('land_concentration', 'land_concentration_lit_source'),     
        ('pdk_v_lit_source', 'pdk_v'),        
        ('pdk_ss_lit_source','pdk_ss'),
        ('pdk_mr_lit_source', 'pdk_mr'),
        
        ('pdk_rz_lit_source', 'pdk_rz'),
        ('s_rastv_lit_source', 's_rastv'),
        ('c_nasish_lit_source', 'c_nasish'),       
        
        ('bpk5_lit_source', 'bpk5'),
        ('xpk_lit_source', 'xpk'),
        
    )
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
    
    def B_inf(self, obj):
        return obj.Binf()[0]    
    
    def number_of_props(self, obj):
        return obj.Binf()[1]
    
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
    

   

