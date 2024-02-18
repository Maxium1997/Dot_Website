from django.urls import path
from . import views
from .views import add_friend

urlpatterns = [
    path('callback', views.callback),
    path('add_friend', add_friend, name='line_bot_add_friend'),
]

