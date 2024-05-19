from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import SignUpView
from .views import logout_view


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", logout_view, name="logout"),
]