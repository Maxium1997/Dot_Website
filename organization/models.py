from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.


class Unit(models.Model):
    name = models.CharField(max_length=20)
    en_name = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="English name"
    )
    serial_number = models.CharField(
        verbose_name='intercom',
        max_length=6,
        blank=True,  # prefer blank to allow empty string
        null=True,
        validators=[MaxLengthValidator(6), MinLengthValidator(0)],
        default=None
    )
    address = models.CharField(max_length=255, blank=True, default=None)
    landline_phone = models.CharField(max_length=10, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)

    superior_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.SET_NULL
    )
    superior_object_id = models.PositiveIntegerField(null=True, blank=True)
    superior = GenericForeignKey('superior_content_type', 'superior_object_id')

    director = models.CharField(max_length=60, blank=True)  # increased length if needed
    deputy_director1 = models.CharField(max_length=60, blank=True)
    deputy_director2 = models.CharField(max_length=60, blank=True)
    deputy_director3 = models.CharField(verbose_name='Chief Secretary', max_length=60, blank=True)

    def get_all_subordinates_direct(self):
        """僅取得下一層的直屬下級單位"""
        from django.contrib.contenttypes.models import ContentType
        unit_type = ContentType.objects.get_for_model(self.__class__)
        return Unit.objects.filter(
            superior_content_type=unit_type,
            superior_object_id=self.id
        )

    @property
    def full_path(self):
        """遞迴取得完整單位路徑"""
        path = [self.name]
        # 呼叫 GenericForeignKey 定義的屬性名稱 (通常是 superior)
        curr = self.superior

        # 限制迴圈深度防止無限循環，並確保父節點仍是 Unit 類型
        limit = 0
        while curr and isinstance(curr, Unit) and limit < 10:
            path.append(curr.name)
            curr = curr.superior
            limit += 1

        return " ".join(reversed(path))

    class Meta:
        constraints = [
            # Example: ensure case-insensitive uniqueness for en_name
            models.UniqueConstraint(models.functions.Lower('en_name'), name='unique_en_name_ci')
        ]

    def __str__(self):
        superior_str = str(self.superior) if self.superior is not None else ''
        name_str = str(self.name)
        return f"{superior_str} {name_str}".strip()

