from django.urls import path, include

from .views import MarketPlaceView


urlpatterns = [
    path('market_place', MarketPlaceView.as_view(), name='market_place'),
    path('market_place/', include([
        path('item/', include([
        ])),
    ])),
]
