from django.db import models
from django.db.models import Q
from django.utils.text import slugify

from organization.models import Unit


class Station(models.Model):
    REGION_NORTH = "north"
    REGION_CENTRAL = "central"
    REGION_SOUTH = "south"
    REGION_EAST = "east"
    REGION_CHOICES = [
        (REGION_NORTH, "北部"),
        (REGION_CENTRAL, "中部"),
        (REGION_SOUTH, "南部"),
        (REGION_EAST, "東部"),
    ]

    name = models.CharField(max_length=100, verbose_name="驛站名稱")
    en_name = models.SlugField(max_length=100, unique=True, verbose_name="英文代稱")
    alias = models.CharField(max_length=100, blank=True, null=True, verbose_name="別名")
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name="區域")
    operator = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="stations",
        verbose_name="承辦單位",
    )
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="聯絡電話")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="緯度"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="經度"
    )
    overview = models.TextField(blank=True, null=True, verbose_name="簡介")
    geo_features = models.TextField(blank=True, null=True, verbose_name="地理特色")
    exhibit_plan = models.TextField(blank=True, null=True, verbose_name="展示規劃")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    def __str__(self):
        return self.name


class StationService(models.Model):
    SERVICE_ACCESSIBLE_TOILET = "accessible_toilet"
    SERVICE_WATER_DISPENSER = "water_dispenser"
    SERVICE_SHOWER = "shower"
    SERVICE_LOCKER = "locker"
    SERVICE_PARKING = "parking"
    SERVICE_LIFE_VEST = "life_vest_rental"
    SERVICE_NURSING_ROOM = "nursing_room"
    SERVICE_CHOICES = [
        (SERVICE_ACCESSIBLE_TOILET, "無障礙廁所"),
        (SERVICE_WATER_DISPENSER, "飲水機"),
        (SERVICE_SHOWER, "沖洗設施"),
        (SERVICE_LOCKER, "置物櫃"),
        (SERVICE_PARKING, "停車場"),
        (SERVICE_LIFE_VEST, "救生衣租借處"),
        (SERVICE_NURSING_ROOM, "哺乳室"),
    ]

    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="驛站",
    )
    service = models.CharField(
        max_length=40, choices=SERVICE_CHOICES, verbose_name="服務功能"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["station", "service"],
                name="unique_station_service",
            )
        ]

    def __str__(self):
        return f"{self.station} - {self.get_service_display()}"


class StationAttraction(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="attractions",
        verbose_name="驛站",
    )
    name = models.CharField(max_length=120, verbose_name="周邊景點")

    def __str__(self):
        return f"{self.station} - {self.name}"


class StationAlbum(models.Model):
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="驛站",
    )
    title = models.CharField(max_length=120, verbose_name="相簿名稱")
    description = models.TextField(blank=True, null=True, verbose_name="相簿描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"{self.station} - {self.title}"


def station_photo_upload_to(instance, filename):
    station_name = slugify(instance.album.station.name, allow_unicode=True) or "station"
    album_title = slugify(instance.album.title, allow_unicode=True) or "album"
    return f"ocean_station/{station_name}/{album_title}/{filename}"


class StationPhoto(models.Model):
    album = models.ForeignKey(
        StationAlbum,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="相簿",
    )
    image = models.ImageField(upload_to=station_photo_upload_to, verbose_name="圖片")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="說明")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="排序")
    is_display = models.BooleanField(default=True, verbose_name="是否顯示")
    is_cover_image = models.BooleanField(default=False, verbose_name="是否為封面")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["album"],
                condition=Q(is_cover_image=True),
                name="unique_album_cover_image",
            )
        ]

    def __str__(self):
        return f"{self.album} - {self.id}"
