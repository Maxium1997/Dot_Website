from django.urls import path
from .views import StartScanAPIView, ScanProgressAPIView

urlpatterns = [
    path("start/", StartScanAPIView.as_view()),

    path("progress/<scan_id>/", ScanProgressAPIView.as_view()),
]
