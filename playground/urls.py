from django.urls import path
from .views import PlaygroundView, KaraokeView, URLtoQRcodeView, pdf_to_word, pdf_to_image
from .views import search_index

app_name = "playground"

urlpatterns = [
    path("", PlaygroundView.as_view(), name="index"),

    path("karaoke/", KaraokeView.as_view(), name="karaoke"),
    path("karaoke/search/", search_index, name="search_song"),

    path("url-to-qr-code/", URLtoQRcodeView.as_view(), name="url_to_qr_code"),
    path("pdf-to-word/", pdf_to_word, name="pdf_to_word"),
    path("pdf-to-image/", pdf_to_image, name="pdf_to_image"),
]
