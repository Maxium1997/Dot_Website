from django.contrib import admin


from .models import OceanStation

# Register your models here.


@admin.register(OceanStation)
class OceanStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'administrative_district', 'address', 'contact_number']
