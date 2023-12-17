from django.contrib import admin


from .models import MobileStorageEquipment, MobileDevice


# Register your models here.
@admin.register(MobileStorageEquipment)
class MobileStorageEquipmentAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'name', 'brand', 'type', 'capacity',
                    'storage_unit', 'manage_unit_content_type', 'manage_unit_object_id',
                    'manager', 'deputy_manager']


@admin.register(MobileDevice)
class MobileDeviceAdmin(admin.ModelAdmin):
    list_display = ['owner', 'owner_unit', 'owner_commission', 'SP_brand', 'SP_model', 'number', 'SW_brand', 'SW_model']
    ordering = ['owner_unit_object_id']
