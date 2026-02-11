from django.urls import path
from .views import (
    ScannerDashboardView,
    StartScanAPIView,
    ScanProgressAPIView,
    ScanAlertsAPIView,
    FinalizeScanAPIView
)

urlpatterns = [
    path("", ScannerDashboardView.as_view(), name="dashboard"),

    path("start/", StartScanAPIView.as_view(), name="scan_start"),
    path("progress/<scan_id>/", ScanProgressAPIView.as_view(), name="scan_progress"),
    path("alerts/", ScanAlertsAPIView.as_view(), name="scan_alerts"),

    path("finalize/<scan_id>/", FinalizeScanAPIView.as_view(), name="finalize_scan"),

]
