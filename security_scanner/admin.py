from django.contrib import admin

from .models import ScanResult, ScanTarget


@admin.register(ScanTarget)
class ScanTargetAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "owner", "created_at")
    ordering = ("-created_at", "name")
    list_filter = ("created_at", "owner")
    search_fields = ("name", "url", "owner__username", "owner__email")


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ("public_id", "target", "high", "medium", "low", "created_at")
    ordering = ("-created_at", "-high", "-medium", "-low")
    list_filter = ("created_at", "target")
    search_fields = ("public_id", "target__name", "target__url")
