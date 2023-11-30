from django.urls import path, include

from .views import BusinessView, MobileStorageEquipmentView
from .views import export_all

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('MobileStorageEquipment', MobileStorageEquipmentView.as_view(), name='mobile_storage_equipments'),
        path('MobileStorageEquipment/', include([
            path('export_all', export_all, name='export_mse_all'),
        ])),
    ])),
]
