from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from organization.definitions import CBUnit, CPC4UnitVer2, ArmyCommission
from .definitions import CertificateUsage, CertificateCustodianClassification, CertificateStorage, CertificateProcess, \
    CertificateUseFor, ItemStatus, OrderStatus

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class CertificateApplication(models.Model):
    USAGE_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateUsage.__members__.values()]
    usage = models.PositiveSmallIntegerField(default=CertificateUsage.Personal.value[0],
                                             choices=USAGE_CHOICES)
    applicant_name = models.CharField(max_length=10, null=False, blank=False)
    applicant_contact_number = models.CharField(max_length=10, null=False, blank=False)
    UNIT_CHOICES = [(_.value[0], _.value[2]) for _ in CPC4UnitVer2.__members__.values()]
    applicant_unit = models.PositiveSmallIntegerField(default=CPC4UnitVer2.Headquarters.value[0],
                                                      choices=UNIT_CHOICES)
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


class Record(models.Model):
    content = models.CharField(max_length=150)
    creator = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    ITEM_STATUS_CHOICES = [(_.value[0], _.value[1]) for _ in ItemStatus.__members__.values()]
    status = models.PositiveSmallIntegerField(default=ItemStatus.Available.value[0],
                                              choices=ITEM_STATUS_CHOICES)
    records = GenericRelation(Record)

    def __str__(self):
        return str(self.name) + str(self.serial_number)


class Order(models.Model):
    serial_number = models.CharField(max_length=20)
    purchaser = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    ORDER_STATUS_CHOICES = [(_.value[0], _.value[1]) for _ in OrderStatus.__members__.values()]
    status = models.PositiveSmallIntegerField(default=OrderStatus.Pending.value[0],
                                              choices=ORDER_STATUS_CHOICES)
    records = GenericRelation(Record)
    items = GenericRelation(Item)

    def __str__(self):
        return self.serial_number
