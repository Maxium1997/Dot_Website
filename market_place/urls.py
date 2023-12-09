from django.urls import path, include

from .views import MarketPlaceView, CertificateApplicationView, CertificateApplicationSearchView


urlpatterns = [
    path('market_place', MarketPlaceView.as_view(), name='market_place'),
    path('market_place/', include([
        path('CertificateApplication', CertificateApplicationView.as_view(), name='certificate_applications'),
        path('CertificateApplication/', include([
            path('search', CertificateApplicationSearchView.as_view(), name='certificate_application_search'),
        ]))
    ])),
]
