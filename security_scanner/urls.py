from django.urls import path
from .views import (
    StartScanAPIView,
    ScanProgressAPIView,
    ScanAlertsAPIView,
)

urlpatterns = [
    path("start/", StartScanAPIView.as_view()),
    path("progress/<scan_id>/", ScanProgressAPIView.as_view()),
    path("alerts/", ScanAlertsAPIView.as_view()),   #新增
]
