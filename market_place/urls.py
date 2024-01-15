from django.urls import path, include

from .views import MarketPlaceView, ItemIndexView, ItemQueryView, ItemStatusQueryView


urlpatterns = [
    path('market_place', MarketPlaceView.as_view(), name='market_place'),
    path('market_place/', include([
        path('item/', include([
            path('dashboard', ItemIndexView.as_view(), name='items_dashboard'),
            path('query/', include([
                path('<str:item_name>', ItemQueryView.as_view(), name='items_query'),
            ])),
            path('status/', include([
                path('<int:item_status>', ItemStatusQueryView.as_view(), name='items_status_query'),
            ])),
        ])),
    ])),
]
