from django.urls import path, include
from . import views

app_name = 'badminton_court_management'


urlpatterns = [
    # 頁面 (Templates)
    path('booking/', views.booking_page, name='booking_page'),

    # API 介面
    path('api/', include([
        path('liff-login/', views.api_liff_login, name='api_liff_login'),
        path('get-gyms/', views.api_get_gyms, name='api_get_gyms'),
        path('get-slots/', views.api_get_slots, name='api_get_slots'),
        path('get-user-balance/', views.api_get_user_balance, name='api_get_user_balance'),
        path('create-booking/', views.api_create_booking, name='api_create_booking'),

        # --- 儲值相關 API ---
        path('create-topup-order/', views.api_create_topup_order, name='api_create_topup_order'),  # 建立訂單並紀錄 Log (方案 B)
    ])),

    path('topup/', views.topup_page, name='topup_page'),  # 儲值方案選擇頁面
    path('topup-order/<str:order_id>/qrcode/', views.topup_order_qrcode, name='topup_order_qrcode'),

    # Staff management
    path('staff', views.staff_gym_dashboard, name='staff_gym_dashboard'),
    path('staff/', include([
        path('gym-staff/', views.staff_gym_staff, name='staff_gym_staff'),
        path('dashboard/', views.staff_gym_dashboard, name='staff_gym_dashboard'),
        path('bookings/<int:booking_id>/cancel/', views.staff_booking_cancel, name='staff_booking_cancel'),
        path('topup/', include([
            path('plans/', views.staff_topup_plans, name='staff_topup_plans'),
            path('plans/<int:plan_id>/deactivate/', views.staff_topup_plan_deactivate, name='staff_topup_plan_deactivate'),
            path('orders/', include([
                path('<str:order_id>/', include([
                    path('verify/', views.staff_topup_verify, name='staff_topup_verify'),
                    path('approve/', views.staff_topup_approve, name='staff_topup_approve'),
                    path('reject/', views.staff_topup_reject, name='staff_topup_reject'),
                ])),
            ])),
        ])),
    ]))
]
