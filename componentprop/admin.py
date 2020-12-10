from django.contrib import admin
from django.db import models
from django.forms import TextInput

from componentprop.models import HazardValueType, HazardCategoryType

@admin.register(HazardValueType)
class HazardValueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'bad_val', 'average_val', 'good_val')
   # list_editable = ('bad_val', 'average_val', 'good_val')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},        
    }


@admin.register(HazardCategoryType)
class HazardValueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category1_item', 'category2_item', 'category3_item', 'category4_item')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},        
    }