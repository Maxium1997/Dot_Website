import datetime
from django.db import models
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

from organization.definitions import CBUnit, CPC4UnitVer2, ArmyCommission
from .definitions import ItemStatus, OrderStatus

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Record(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    creator = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.content_object} on {self.created_time}"

    class Meta:
        ordering = ['-created_time']


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

    def save(self, *args, **kwargs):
        # now_date = datetime.date.today().isoformat()
        # now_date_order_num = Order.objects.filter(serial_number__icontains=now_date).count
        # self.serial_number = now_date + "-" + str(now_date_order_num+1)
        super().save(*args, **kwargs)

        # Create a LogEntry for the change
        content_type = ContentType.objects.get_for_model(self)
        # Create a History entry
        Record.objects.create(
            content_type=content_type,
            object_id=self.id,
            content_object=self,
            content=self.content,
            creator=self.serial_number,  # Set the creator information
        )

    def __str__(self):
        return self.serial_number
