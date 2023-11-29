from django.contrib import admin


from .models import MobileStorageEquipment


# Register your models here.
@admin.register(MobileStorageEquipment)
class MobileStorageEquipmentAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'name', 'brand', 'type', 'capacity',
                    'storage_unit', 'manage_unit',
                    'manager', 'deputy_manager']
