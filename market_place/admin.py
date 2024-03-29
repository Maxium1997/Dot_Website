from django.contrib import admin

from .models import CertificateApplication, Category, Item
# Register your models here.


@admin.register(CertificateApplication)
class CertificateApplicationAdmin(admin.ModelAdmin):
    list_display = ['usage',
                    'applicant_name', 'applicant_contact_number', 'applicant_unit', 'applicant_address',
                    'custodian_commission', 'custodian_name', 'custodian_ID_number', 'custodian_contact_number',
                    'custodian_email', 'custodian_classification',
                    'storage', 'process', 'use_for', 'applied_date', 'edited_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'serial_number', 'status']
