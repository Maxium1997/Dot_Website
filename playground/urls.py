from django.urls import path, include

from .views import PlaygroundView, KaraokeView
from .views import search_index, URLtoQRcodeView


urlpatterns = [
    path('playground', PlaygroundView.as_view(), name='playground'),
    path('playground/', include([
        path('karaoke', KaraokeView.as_view(), name='karaoke'),
        path('karaoke/', include([
            path('search', search_index, name='search_song'),
        ])),

        path('url-to-qr-code', URLtoQRcodeView.as_view(), name='url_to_qr_code'),
    ])),
]
