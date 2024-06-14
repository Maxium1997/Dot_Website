from django.contrib import admin


from .models import OceanStation


@admin.register(OceanStation)
class OceanStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'administrative_district', 'address', 'contact_number']
