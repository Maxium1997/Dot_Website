from django import forms
from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from organization.models import Unit
from .models import (
    Station,
    StationAlbum,
    StationAttraction,
    StationPhoto,
    StationService,
)


class StationResource(resources.ModelResource):
    operator = fields.Field(
        column_name="operator",
        attribute="operator",
        widget=ForeignKeyWidget(Unit, "id"),
    )

    class Meta:
        model = Station
        fields = (
            "id",
            "name",
            "en_name",
            "alias",
            "region",
            "operator",
            "address",
            "phone",
            "latitude",
            "longitude",
            "overview",
            "geo_features",
            "exhibit_plan",
        )
        import_id_fields = ("en_name",)


class StationServiceResource(resources.ModelResource):
    station = fields.Field(
        column_name="station",
        attribute="station",
        widget=ForeignKeyWidget(Station, "en_name"),
    )

    class Meta:
        model = StationService
        fields = ("id", "station", "service")


class StationAttractionResource(resources.ModelResource):
    station = fields.Field(
        column_name="station",
        attribute="station",
        widget=ForeignKeyWidget(Station, "en_name"),
    )

    class Meta:
        model = StationAttraction
        fields = ("id", "station", "name")


class StationAlbumResource(resources.ModelResource):
    station = fields.Field(
        column_name="station",
        attribute="station",
        widget=ForeignKeyWidget(Station, "en_name"),
    )

    class Meta:
        model = StationAlbum
        fields = ("id", "station", "title", "description", "created_at")


class StationAdminForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=StationService.SERVICE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="服務功能",
    )

    class Meta:
        model = Station
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["services"].initial = list(
                self.instance.services.values_list("service", flat=True)
            )


class StationAttractionInline(admin.TabularInline):
    model = StationAttraction
    extra = 1


class StationAlbumInline(admin.TabularInline):
    model = StationAlbum
    extra = 0


@admin.register(Station)
class StationAdmin(ImportExportModelAdmin):
    form = StationAdminForm
    resource_class = StationResource
    list_display = ("name", "region", "operator", "phone")
    list_filter = ("region", "operator")
    search_fields = ("name", "en_name", "alias", "address", "phone")
    inlines = [StationAttractionInline, StationAlbumInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        selected = set(form.cleaned_data.get("services", []))
        current = set(obj.services.values_list("service", flat=True))
        to_add = selected - current
        to_remove = current - selected
        if to_remove:
            StationService.objects.filter(station=obj, service__in=to_remove).delete()
        for service in to_add:
            StationService.objects.create(station=obj, service=service)


class StationPhotoInline(admin.TabularInline):
    model = StationPhoto
    extra = 1
    fields = ("image", "caption", "sort_order", "is_display", "is_cover_image")


@admin.register(StationAlbum)
class StationAlbumAdmin(ImportExportModelAdmin):
    resource_class = StationAlbumResource
    list_display = ("title", "station", "created_at")
    list_filter = ("station",)
    search_fields = ("title", "station__name")
    inlines = [StationPhotoInline]


@admin.register(StationService)
class StationServiceAdmin(ImportExportModelAdmin):
    resource_class = StationServiceResource
    list_display = ("station", "service")
    list_filter = ("service",)
    search_fields = ("station__name",)


@admin.register(StationAttraction)
class StationAttractionAdmin(ImportExportModelAdmin):
    resource_class = StationAttractionResource
    list_display = ("station", "name")
    search_fields = ("station__name", "name")


@admin.register(StationPhoto)
class StationPhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "is_display", "is_cover_image")
    list_filter = ("is_display", "is_cover_image")
    search_fields = ("album__title", "album__station__name", "caption")
