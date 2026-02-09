from rest_framework import serializers
from .models import ScanTarget


class ScanTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanTarget
        fields = ["id", "name", "url", "created_at"]
