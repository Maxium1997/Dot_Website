from django.urls import path, include

from .views import MarketPlaceView, ItemIndexView, ItemQueryView, ItemStatusQueryView, \
    MaintenanceManagementView, OrderDashboardView, OrderDetailView, ItemReportView, \
    order_confirm


urlpatterns = [
    path('market_place', MarketPlaceView.as_view(), name='market_place'),
    path('market_place/', include([
        path('item/', include([
            path('dashboard', ItemIndexView.as_view(), name='items_dashboard'),
            path('report', ItemReportView.as_view(), name='item_report'),

            path('query/', include([
                path('<str:item_name>', ItemQueryView.as_view(), name='items_query'),
            ])),
            path('status/', include([
                path('<int:item_status>', ItemStatusQueryView.as_view(), name='items_status_query'),
            ])),
        ])),

        path('maintenance_management', MaintenanceManagementView.as_view(), name='maintenance_management'),
        path('maintenance_management/', include([
            path('order/', include([
                path('dashboard', OrderDashboardView.as_view(), name='order_dashboard'),
                path('<str:serial_number>/', include([
                    path('detail', OrderDetailView.as_view(), name='order_detail'),
                    path('confirm', order_confirm, name='order_confirm'),
                ]))
            ]))
        ])),
    ])),
]
