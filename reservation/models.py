from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.


class Undefined(models.Model):  # class名稱尚未決定
    source_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    source_object_id = models.PositiveIntegerField(null=True, blank=True)
