from django.contrib import admin

from chemcomponent.models import WasteComponent

@admin.register(WasteComponent)
class WasteComponentAdmin(admin.ModelAdmin):
    list_display = ('name','chemical_type', 'W')

    def W(self, obj):
        return obj.get_w()

#admin.site.register(WasteComponent)