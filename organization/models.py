from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class BasicOrg(models.Model):
    name = models.CharField()
    en_name = models.CharField()
    slug = models.SlugField()
    address = models.CharField()
    landline_phone = models.CharField()
    director = models.CharField(null=False, blank=False)
    deputy_director1 = models.CharField(null=False, blank=False)
    deputy_director2 = models.CharField(null=True, blank=True)
    deputy_director3 = models.CharField(null=True, blank=True)


class Administration(models.Model):
    business_units = GenericRelation
    duty_units = GenericRelation
    dispatch_units = GenericRelation


class Branch(BasicOrg):
    business_units = GenericRelation
    duty_units = GenericRelation


class CoastPatrolCorps(BasicOrg):
    superior_authority = models.ForeignKey(Branch, on_delete=models.PROTECT,
                                           null=False, blank=False)


class InspectionOffice(BasicOrg):
    superior_authority = models.ForeignKey(CoastPatrolCorps, on_delete=models.PROTECT,
                                           null=False, blank=False)
