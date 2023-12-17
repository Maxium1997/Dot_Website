from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from organization.definitions import CPC4Unit, ArmyCommission
from business.definitions import EquipmentType, StorageUnit

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class SubcategoryDetail(models.Model):
    sub_category = models.ForeignKey(Subcategory, on_delete=models.PROTECT, null=True)


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
