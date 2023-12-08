from django.urls import path, include

from .views import MarketPlaceView, CertificateApplicationView


urlpatterns = [
    path('market_place', MarketPlaceView.as_view(), name='market_place'),
    path('market_place/', include([
        path('certificate', CertificateApplicationView.as_view(), name='certificate_applications'),
    ])),
]
