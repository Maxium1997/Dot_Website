from django.db import models

# Create your models here.


class Item(models.Model):
    serial_number = models.CharField
    name = models.CharField
    brand = models.CharField
    model = models.CharField
    # use_unit =
    # manage_unit =
    # storage_place =
    # manager =


class Property(Item):
    pass


class Equipment(Item):
    pass
