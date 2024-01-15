from django.contrib import admin


from .models import MobileStorageEquipment, MobileDevice, CertificateApplication


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


@admin.register(CertificateApplication)
class CertificateApplicationAdmin(admin.ModelAdmin):
    list_display = ['usage',
                    'applicant_name', 'applicant_contact_number', 'applicant_unit', 'applicant_address',
                    'custodian_commission', 'custodian_name', 'custodian_ID_number', 'custodian_contact_number',
                    'custodian_email', 'custodian_classification',
                    'storage', 'process', 'use_for', 'applied_date', 'edited_date']
