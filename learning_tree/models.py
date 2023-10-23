from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from website.models import TaggedItem

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class Subject(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = GenericRelation(TaggedItem)

    def __str__(self):
        return self.name
