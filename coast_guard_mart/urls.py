from django.urls import path, include

from . import views

app_name = 'coast_guard_mart'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('', include([
        path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),

        path('product/', include([
            path('list/', views.product_list, name='product_list'),
            path('<int:pk>/', views.product_detail, name='product_detail'),
        ])),

        path('cart/', views.cart_detail, name='cart_detail'),
        path('cart/', include([
            path('add-to-cart-bulk/', views.add_to_cart_bulk, name='add_to_cart_bulk'),
            path('add-to-cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
            path('remove/<str:cart_key>/', views.remove_from_cart, name='remove_from_cart'),
            path('checkout/', views.checkout, name='checkout'),
        ])),

        path('my-orders/', views.order_list, name='order_list'),
        path('order/', include([
            path('<str:order_id>/', views.order_detail, name='order_detail'),
            path('cancel/<str:order_id>/', views.cancel_order, name='cancel_order'),

            path('order/qrcode/<str:order_id>/', views.generate_order_qrcode, name='generate_order_qrcode'),
            path('order/verify-complete/<str:order_id>/', views.staff_verify_order_complete, name='staff_verify_order_complete'),
        ])),

        path('claim-credit/', views.claim_credit, name='claim_credit'),
        path('api/units/<int:unit_id>/subordinates/', views.api_get_subordinates, name='api_get_subordinates'),

        path('staff/', include([
            path('dashboard/', views.staff_order_dashboard, name='staff_order_dashboard'),
            path('inventory/', views.staff_inventory_summary, name='staff_inventory_summary'),
            path('inventory/export/', views.export_inventory_excel, name='export_inventory_excel'),

            path('whitelist/', include([
                path('list/', views.staff_whitelist_manager, name='staff_whitelist_manager'),
                path('add/', views.staff_whitelist_add, name='staff_whitelist_add'),
                path('remove/', views.staff_whitelist_delete, name='staff_whitelist_delete'),
                path('import/', views.staff_whitelist_import, name='staff_whitelist_import'),
                path('export/', views.staff_whitelist_export, name='staff_whitelist_export'),
                path('template/', views.download_whitelist_template, name='staff_whitelist_template_download'),
            ])),
        ])),

        path('api/sub-units/', views.api_get_sub_units, name='api_get_sub_units'),
    ]))
]

