from django.urls import path

from . import views

app_name = "ocean_station"

urlpatterns = [
    path("", views.index, name="index"),
]
