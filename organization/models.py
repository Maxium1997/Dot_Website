from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from .definitions import Classification

# Create your models here.


class BasicOrgInfo(models.Model):
    name = models.CharField(max_length=20)
    en_name = models.CharField(max_length=255, unique=True)
    serial_number = models.CharField(verbose_name='intercom', max_length=6, null=True, blank=True)  # 海巡6碼
    director = models.CharField(max_length=10, null=False, blank=False)
    deputy_director1 = models.CharField(max_length=10, null=True, blank=True)
    deputy_director2 = models.CharField(max_length=10, null=True, blank=True)
    deputy_director3 = models.CharField(verbose_name='Chief Secretary', max_length=10, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


# 組、室
class Division(BasicOrgInfo):
    superior_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    superior_object_id = models.PositiveIntegerField(null=True, blank=True)
    superior = GenericForeignKey('superior_content_type', 'superior_object_id')

    def __str__(self):
        return str(self.superior) + " " + str(self.name)


# 科、室
class Section(BasicOrgInfo):
    superior_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    superior_object_id = models.PositiveIntegerField(null=True, blank=True)
    superior = GenericForeignKey('superior_content_type', 'superior_object_id')

    def __str__(self):
        return str(self.superior) + " " + str(self.name)


# 海巡署
class Administration(BasicOrgInfo):
    address = models.CharField(max_length=255, null=True, blank=True)
    landline_phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return str(self.name)


# 分署
class Branch(BasicOrgInfo):
    address = models.CharField(max_length=255, null=True, blank=True)
    landline_phone = models.CharField(max_length=10, null=True, blank=True)
    superior = models.ForeignKey(Administration, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.superior.name) + " " + str(self.name)


# 巡防區
class PatrolAreaOffice(BasicOrgInfo):
    CLASSIFICATION_CHOICES = [(_.value[0], _.value[1]) for _ in Classification.__members__.values()]
    number = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICES)
    superior = models.ForeignKey(Administration, null=True, blank=True, on_delete=models.SET_NULL)
    # 合署辦公單位
    dispatch_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    dispatch_object_id = models.PositiveIntegerField(null=True, blank=True)
    dispatch = GenericForeignKey('dispatch_content_type', 'dispatch_object_id')
    # 轄區
    administrative_region = models.CharField(max_length=5, null=True, blank=True)
    # 指揮運用單位(海巡隊、岸巡隊及查緝隊)，以下尚未完成規劃
    # command_integrations = GenericRelation()

    def __str__(self):
        return self.name


# 作業隊、中隊
class Brigade(BasicOrgInfo):
    CLASSIFICATION_CHOICES = [(_.value[0], _.value[1]) for _ in Classification.__members__.values()]
    number = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICES, null=True, blank=True)
    # 上級機關
    superior = models.ForeignKey(Administration, null=True, blank=True, on_delete=models.SET_NULL)
    # 派駐機關
    garrison = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# 岸巡隊
class CoastPatrolCorps(BasicOrgInfo):
    address = models.CharField(max_length=255, null=True, blank=True)
    landline_phone = models.CharField(max_length=10, null=True, blank=True)
    central_exchange_intercom = models.CharField(max_length=6, null=True, blank=True)
    superior = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.superior.name) + " " + str(self.name)


# 轄屬岸巡隊的單位（eg.一二組、中隊部、勤務分隊、通資小隊等等）
class InternalUnit(BasicOrgInfo):
    superior = models.ForeignKey(CoastPatrolCorps, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.superior.name) + " " + str(self.name)


# 機動巡邏站
class PatrolStation(BasicOrgInfo):
    CLASSIFICATION_CHOICES = [(_.value[0], _.value[1]) for _ in Classification.__members__.values()]
    number = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    landline_phone = models.CharField(max_length=10, null=True, blank=True)    # 自動線
    email = models.EmailField(null=True, blank=True)     # 單位信箱
    superior = models.ForeignKey(InternalUnit, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class InspectionOffice(BasicOrgInfo):
    address = models.CharField(max_length=255, null=True, blank=True)
    landline_phone = models.CharField(max_length=10, null=True, blank=True)    # 自動線
    email = models.EmailField(null=True, blank=True)     # 單位信箱
    superior = models.ForeignKey(CoastPatrolCorps, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.name
