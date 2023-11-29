from django.urls import path, include

from .views import BusinessView, MobileStorageEquipmentView

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    path('business/', include([
        path('MobileStorageEquipment', MobileStorageEquipmentView.as_view(), name='mobile_storage_equipments'),
    ])),
]
