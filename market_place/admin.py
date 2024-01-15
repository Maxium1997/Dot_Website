from django.contrib import admin

from .models import Category, Item
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'serial_number', 'status']
