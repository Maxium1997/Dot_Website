from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from organization.definitions import CPC4Unit, ArmyCommission
from business.definitions import EquipmentType, StorageUnit, CertificateUsage, CertificateCustodianClassification, \
    CertificateStorage, CertificateProcess, CertificateUseFor, \
    OceanStationServiceItems

# Create your models here.


class MobileStorageEquipment(models.Model):
    serial_number = models.CharField(max_length=9, null=True, blank=True)
    name = models.CharField(max_length=20, null=False, blank=False)
    builtin_memory = models.BooleanField(default=False)
    brand = models.CharField(max_length=20, null=True, blank=True)
    EQUIPMENT_TYPES = [(_.value[0], _.value[1]) for _ in EquipmentType.__members__.values()]
    type = models.PositiveSmallIntegerField(null=False, blank=False,
                                            default=EquipmentType.other.value[0],
                                            choices=EQUIPMENT_TYPES)
    model = models.CharField(max_length=20, null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(null=True, blank=True)
    STORAGE_UNIT_CHOICES = [(_.value[0], _.value[1]) for _ in StorageUnit.__members__.values()]
    storage_unit = models.PositiveSmallIntegerField(null=True, blank=True,
                                                    choices=STORAGE_UNIT_CHOICES)
    # resource =
    # resource_date =
    # is_private = models.BooleanField(default=False)
    manage_unit_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    manage_unit_object_id = models.PositiveIntegerField(null=True, blank=True)
    manage_unit = GenericForeignKey('manage_unit_content_type', 'manage_unit_object_id')
    manager = models.CharField(max_length=10)
    deputy_manager = models.CharField(max_length=10)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + str(self.serial_number)


class MobileDevice(models.Model):
    owner = models.CharField(max_length=10)

    owner_unit_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    owner_unit_object_id = models.PositiveIntegerField(null=True, blank=True)
    owner_unit = GenericForeignKey('owner_unit_content_type', 'owner_unit_object_id')

    ARMY_COMMISSION_CHOICES = [(_.value[0], _.value[1]) for _ in ArmyCommission.__members__.values()]
    owner_commission = models.PositiveIntegerField(default=ArmyCommission.NonSet.value[0],
                                                   choices=ARMY_COMMISSION_CHOICES,
                                                   null=False, blank=False)
    # SP = Smart Phone
    SP_brand = models.CharField(max_length=20, null=True, blank=True)
    SP_model = models.CharField(max_length=20, null=True, blank=True)
    # SW = Smart Watch
    SW_brand = models.CharField(max_length=20, null=True, blank=True)
    SW_model = models.CharField(max_length=20, null=True, blank=True)
    number = models.CharField(max_length=10, unique=True, null=True, blank=True)    # phone number


class MobileDeviceList(models.Model):
    MANAGE_UNIT_CHOICES = [(_.value[0], _.value[1]) for _ in CPC4Unit.__members__.values()]
    manage_unit = models.PositiveIntegerField(default=CPC4Unit.CIE_squad.value[0],
                                              choices=MANAGE_UNIT_CHOICES)
    manager = models.CharField(max_length=10)
    remarks = models.TextField(null=True, blank=True)
    items = GenericRelation(MobileDevice)


class CertificateApplication(models.Model):
    USAGE_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateUsage.__members__.values()]
    usage = models.PositiveSmallIntegerField(default=CertificateUsage.Personal.value[0],
                                             choices=USAGE_CHOICES)
    applicant_name = models.CharField(max_length=10, null=False, blank=False)
    applicant_contact_number = models.CharField(max_length=10, null=False, blank=False)

    applicant_unit_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    applicant_unit_object_id = models.PositiveIntegerField(null=True, blank=True)
    applicant_unit = GenericForeignKey('applicant_unit_content_type', 'applicant_unit_object_id')

    applicant_address = models.CharField(max_length=255, null=False, blank=False)
    ARMY_COMMISSION_CHOICES = [(_.value[0], _.value[1]) for _ in ArmyCommission.__members__.values()]
    custodian_commission = models.PositiveIntegerField(default=ArmyCommission.NonSet.value[0],
                                                       choices=ARMY_COMMISSION_CHOICES)
    custodian_name = models.CharField(max_length=10, null=False, blank=False)
    custodian_ID_number = models.CharField(max_length=10, null=False, blank=False)
    custodian_contact_number = models.CharField(max_length=10, null=False, blank=False)
    custodian_email = models.CharField(max_length=255, null=False, blank=False)
    CLASSIFICATION_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateCustodianClassification.__members__.values()]
    custodian_classification = models.PositiveSmallIntegerField(default=CertificateCustodianClassification.Unit.value[0],
                                                                choices=CLASSIFICATION_CHOICES)
    STORAGE_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateStorage.__members__.values()]
    storage = models.PositiveSmallIntegerField(default=CertificateStorage.ICCard.value[0],
                                               choices=STORAGE_CHOICES)
    PROCESS_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateProcess.__members__.values()]
    process = models.PositiveSmallIntegerField(default=CertificateProcess.Apply.value[0],
                                               choices=PROCESS_CHOICES)
    USE_FOR_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateUseFor.__members__.values()]
    use_for = models.PositiveSmallIntegerField(default=CertificateUseFor.Business.value[0],
                                               choices=USE_FOR_CHOICES)
    applied_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)


class OceanStation(models.Model):
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

