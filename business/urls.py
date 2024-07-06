from django.urls import path, include

from .views import BusinessView

from .views import OceanStationIndexView, OceanStationDetailView, OceanStationUpdateView,OceanStationCoverPhotoUploadView
from .views import import_ocean_station

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('OceanStation', OceanStationIndexView.as_view(), name='ocean_stations'),
        path('OceanStation/', include([
            path('<str:ocean_station_name>/', include([
                path('detail', OceanStationDetailView.as_view(), name='ocean_station_detail'),
                path('update', OceanStationUpdateView.as_view(), name='ocean_station_update'),
                path('cover_photo_upload', OceanStationCoverPhotoUploadView.as_view(), name='ocean_station_cover_photo_upload'),
            ])),
            path('import', import_ocean_station, name='import_ocean_station'),
        ])),
    ])),
]
