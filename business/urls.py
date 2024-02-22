from django.urls import path, include

from .views import BusinessView, MobileStorageEquipmentView, MobileStorageEquipmentFilteredView, \
    MobileDeviceView, MobileDeviceFilteredView, CertificateApplicationView, CertificateApplicationSearchView

from .views import OceanStationIndexView, OceanStationUpdateView
from .views import import_ocean_station

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('MobileStorageEquipment', MobileStorageEquipmentView.as_view(), name='mobile_storage_equipments'),
        path('MobileStorageEquipment/', include([
            path('filtered/', MobileStorageEquipmentFilteredView.as_view(), name='mse_filtered'),
        ])),

        path('MobileDevice', MobileDeviceView.as_view(), name='mobile_devices'),
        path('MobileDevice/', include([
            path('filtered/', MobileDeviceFilteredView.as_view(), name='md_filtered'),
        ])),

        path('CertificateApplication', CertificateApplicationView.as_view(), name='certificate_applications'),
        path('CertificateApplication/', include([
            path('search', CertificateApplicationSearchView.as_view(), name='certificate_application_search'),
        ])),

        path('OceanStation', OceanStationIndexView.as_view(), name='ocean_stations'),
        path('OceanStation/', include([
            path('<str:ocean_station_name>/', include([
                path('update', OceanStationUpdateView.as_view(), name='ocean_station_update'),
            ])),
            path('import', import_ocean_station, name='import_ocean_station'),
        ])),
    ])),
]
