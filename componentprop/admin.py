from django.contrib import admin

from componentprop.models import HazardValueType, HazardCategoryType

@admin.register(HazardValueType)
class HazardValueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'bad_val', 'average_val', 'good_val')

@admin.register(HazardCategoryType)
class HazardValueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category1_item', 'category2_item', 'category3_item', 'category4_item')