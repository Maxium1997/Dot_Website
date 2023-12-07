from django.urls import path, include

from .views import BusinessView, MobileStorageEquipmentView, MobileStorageEquipmentFilteredView, \
    MobileDeviceView
from .views import export_mse_all

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('MobileStorageEquipment', MobileStorageEquipmentView.as_view(), name='mobile_storage_equipments'),
        path('MobileStorageEquipment/', include([
            path('export_mse_all', export_mse_all, name='export_mse_all'),
            path('filtered/', MobileStorageEquipmentFilteredView.as_view(), name='mse_filtered'),
        ])),

        path('MobileDevice', MobileDeviceView.as_view(), name='mobile_devices'),
    ])),
]
