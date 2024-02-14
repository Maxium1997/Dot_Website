from django.urls import path, include

from .views import PlaygroundView, KaraokeView
from .views import search_index


urlpatterns = [
    path('playground', PlaygroundView.as_view(), name='playground'),
    path('playground/', include([
        path('karaoke', KaraokeView.as_view(), name='karaoke'),
        path('karaoke', include([
            path('search', search_index, name='search_song'),
        ])),
    ])),
]
