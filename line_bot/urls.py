from django.urls import path
from . import views
# from .views import home

urlpatterns = [
    # path('home', home, name='line_bot'),
    path('callback', views.callback)
]
