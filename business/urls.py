from django.urls import path, include

from .views import BusinessView, MobileStorageEquipmentView, MobileStorageEquipmentFilteredView, \
    MobileDeviceView, MobileDeviceFilteredView
from .views import export_mse_all, process_excel

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('MobileStorageEquipment', MobileStorageEquipmentView.as_view(), name='mobile_storage_equipments'),
        path('MobileStorageEquipment/', include([
            path('export_mse_all', export_mse_all, name='export_mse_all'),
            path('filtered/', MobileStorageEquipmentFilteredView.as_view(), name='mse_filtered'),
        ])),

        path('MobileDevice', MobileDeviceView.as_view(), name='mobile_devices'),
        path('MobileDevice/', include([
            # Modified the MD models, but process excel function does not rewrite.
            # path('import_md_excel', process_excel, name='process_excel'),
            path('filtered/', MobileDeviceFilteredView.as_view(), name='md_filtered'),
        ])),
    ])),
]
