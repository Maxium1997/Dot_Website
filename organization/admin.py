from django.contrib import admin

from .models import Administration, Branch, CoastPatrolCorps, InternalUnit, InspectionOffice, PatrolStation, Brigade
# Register your models here.


@admin.register(Administration)
class AdministrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'director', 'deputy_director1', 'deputy_director2', 'deputy_director3']


@admin.register(CoastPatrolCorps)
class CoastPatrolCorpsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'address', 'landline_phone', 'central_exchange_intercom']


@admin.register(InternalUnit)
class InternalUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'serial_number', 'director', 'deputy_director1']
    ordering = ['serial_number']


@admin.register(InspectionOffice)
class InspectionOfficeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'address', 'landline_phone', 'intercom_phone']
    ordering = ['intercom_phone']


@admin.register(PatrolStation)
class PatrolStationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'address', 'landline_phone', 'intercom_phone']
    ordering = ['intercom_phone']
