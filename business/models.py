import os
import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from business.definitions import EquipmentType, StorageUnit, CertificateUsage, CertificateCustodianClassification, \
    CertificateStorage, CertificateProcess, CertificateUseFor, \
    OceanStationServiceItems

# Create your models here.

logger = logging.getLogger(__name__)


class OceanStation(models.Model):
    def _image_upload_path(self, filename):
        return os.path.join("Ocean_Stations/%s/cover_photo/" % self.name, filename)

    cover_photo = models.ImageField(upload_to=_image_upload_path, null=True)
    oid = models.CharField(max_length=150, null=False, blank=False, unique=True)
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

    def delete_old_cover_photo(self):
        if self.cover_photo and os.path.isfile(self.cover_photo.path):
            try:
                os.remove(self.cover_photo.path)
                logger.info(f"Deleted old cover photo: {self.cover_photo.path}")
            except Exception as e:
                logger.error(f"Error deleting old cover photo: {e}")

    def __str__(self):
        return self.name

