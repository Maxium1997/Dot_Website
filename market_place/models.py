from django.db import models

from organization.definitions import CBUnit, ArmyCommission
from .definitions import CertificateUsage, CertificateCustodianClassification, CertificateStorage, CertificateProcess, \
    CertificateUseFor

# Create your models here.


class CertificateApplication(models.Model):
    USAGE_CHOICES = [(_.value[0], _.value[1]) for _ in CertificateUsage.__members__.values()]
    usage = models.PositiveSmallIntegerField(default=CertificateUsage.Personal.value[0],
                                             choices=USAGE_CHOICES)
    applicant_name = models.CharField(max_length=10, null=False, blank=False)
    applicant_contact_number = models.CharField(max_length=10, null=False, blank=False)
    UNIT_CHOICES = [(_.value[0], _.value[1]) for _ in CBUnit.__members__.values()]
    applicant_unit = models.PositiveSmallIntegerField(default=CBUnit.CPC4.value[0],
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
