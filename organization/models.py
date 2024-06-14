from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from .definitions import Classification

# Create your models here.


class Head(models.Model):
    name = models.CharField(max_length=128)     # 中文名稱
    en_name = models.CharField(max_length=255, unique=True)     # 英文名稱
    business_ID_number = models.CharField(max_length=10, unique=True)   # 統一編號
    responsible_person = models.CharField(max_length=10)    # 負責人
    deputy_director1 = models.CharField(max_length=10, null=True, blank=True)   # 第一職務代理人
    deputy_director2 = models.CharField(max_length=10, null=True, blank=True)   # 第二職務代理人
    deputy_director3 = models.CharField(verbose_name='Chief Secretary', max_length=10, null=True, blank=True)   # 第三職務代理人
    address = models.CharField(max_length=255, null=True, blank=True)   # 地址
    address_longitude = models.CharField(max_length=10, null=True, blank=True)      # 經度
    address_latitude = models.CharField(max_length=10, null=True, blank=True)       # 緯度
    telephone = models.CharField(max_length=11, null=True, blank=True)  # 自動線
    extension_number = models.CharField(max_length=6, null=True, blank=True)  # 分機/海巡六碼
    fax_number = models.CharField(max_length=11)    # 傳真電話
    email = models.EmailField(null=True, blank=True)  # 單位信箱
    official_website = models.URLField()    # 官方網站

    objects = models.Manager()

    def __str__(self):
        return self.name


class Branch(Head):
    superior_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    superior_object_id = models.PositiveIntegerField(null=True, blank=True)
    superior = GenericForeignKey('superior_content_type', 'superior_object_id')

    def __str__(self):
        return str(self.superior) + " " + str(self.name)


class Department(models.Model):
    name = models.CharField(max_length=128)  # 中文名稱
    en_name = models.CharField(max_length=255)  # 英文名稱
    chief = models.CharField(max_length=128, null=True, blank=True)
    superior_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    superior_object_id = models.PositiveIntegerField(null=True, blank=True)
    superior = GenericForeignKey('superior_content_type', 'superior_object_id')
