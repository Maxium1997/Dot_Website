import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from organization.definitions import CPC4Unit, ArmyCommission
from business.definitions import EquipmentType, StorageUnit, CertificateUsage, CertificateCustodianClassification, \
    CertificateStorage, CertificateProcess, CertificateUseFor, \
    OceanStationServiceItems

# Create your models here.


class OceanStation(models.Model):
    def _image_upload_path(self, filename):
        return os.path.join("Ocean_Stations/%s/cover_photo/" % self.name, filename)

    cover_photo = models.ImageField(upload_to=_image_upload_path, null=True)
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)
    manage_administration_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    manage_administration_object_id = models.PositiveIntegerField(null=True, blank=True)
    manage_administration_content_object = GenericForeignKey('manage_administration_content_type', 'manage_administration_object_id')
    administrative_district = models.CharField(max_length=5, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    coordinate_longitude = models.CharField(max_length=12, null=True, blank=True)
    coordinate_latitude = models.CharField(max_length=12, null=True, blank=True)
    service_items = models.PositiveSmallIntegerField(default=OceanStationServiceItems.Lounge.value[0])
    fans_page_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

