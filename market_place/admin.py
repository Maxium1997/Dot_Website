from django.contrib import admin

from .models import Category, Item, Order, Record
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'serial_number', 'status']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'purchaser', 'status']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'creator', 'created_time']
