from django.db import models
from django.conf import settings


class ScanTarget(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scan_targets"
    )
    name = models.CharField(max_length=100)
    url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ScanResult(models.Model):
    target = models.ForeignKey(
        ScanTarget,
        on_delete=models.CASCADE,
        related_name="results"
    )

    scan_id = models.CharField(max_length=50)

    high = models.IntegerField(default=0)
    medium = models.IntegerField(default=0)
    low = models.IntegerField(default=0)

    report_json = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

