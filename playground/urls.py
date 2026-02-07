from django.urls import path
from .views import PlaygroundView, KaraokeView, URLtoQRcodeView
from .views import search_index

app_name = "playground"

urlpatterns = [
    path("", PlaygroundView.as_view(), name="index"),

    path("karaoke/", KaraokeView.as_view(), name="karaoke"),
    path("karaoke/search/", search_index, name="search_song"),

    path("url-to-qr-code/", URLtoQRcodeView.as_view(), name="url_to_qr_code"),
]
