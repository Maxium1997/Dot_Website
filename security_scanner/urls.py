from django.urls import path
from .views import StartScanAPIView

urlpatterns = [
    path("start/", StartScanAPIView.as_view()),
]
