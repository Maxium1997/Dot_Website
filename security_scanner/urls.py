from django.urls import path
from .views import start_scan

urlpatterns = [
    path("scan/start/", start_scan),
]
