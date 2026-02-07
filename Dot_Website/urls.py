"""Dot_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Register security audit signal handlers (NIST/ISO)
import Dot_Website.security_signals  # noqa: F401, E402

urlpatterns = [
    path('', include('website.urls')),

    path('admin/', admin.site.urls),

    # 優先處理 allauth (LINE 登入相關)
    path('accounts/', include('allauth.urls')),

    # 處理自定義的 signup 和 logout
    path('accounts/', include('registration.urls')),

    # 處理 Django 內建登入 (如果 registration 沒寫 login，就由這裡提供)
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include('organization.urls')),
    path("playground/", include("playground.urls")),
    path('coast_guard_mart/', include('coast_guard_mart.urls')),
    path('line_bot/', include('line_bot.urls')),
    path('badminton_court_management/', include('badminton_court_management.urls')),
    path('ocean_station/', include('ocean_station.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def error_403(request, exception=None):
    return render(request, "403.html", status=403)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    context = {}
    if getattr(settings, "SHOW_ERROR_TRACEBACK", False) and request.user.is_staff:
        context["error_traceback"] = getattr(request, "_error_traceback", "")
    return render(request, "500.html", context=context, status=500)


handler403 = error_403
handler404 = error_404
handler500 = error_500
