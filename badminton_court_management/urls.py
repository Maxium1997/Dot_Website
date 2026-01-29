from django.urls import path, include
from . import views

app_name = 'badminton_court_management'

urlpatterns = [
    # 頁面 (Templates)
    path('booking/', views.booking_page, name='booking_page'),
    path('topup/', views.topup_page, name='topup_page'),  # 儲值方案選擇頁面

    # API 介面
    path('api/', include([
        path('liff-login/', views.api_liff_login, name='api_liff_login'),
        path('get-gyms/', views.api_get_gyms, name='api_get_gyms'),
        path('get-slots/', views.api_get_slots, name='api_get_slots'),
        path('get-user-balance/', views.api_get_user_balance, name='api_get_user_balance'),
        path('create-booking/', views.api_create_booking, name='api_create_booking'),

        # --- 儲值相關 API ---
        path('create-topup-order/', views.api_create_topup_order, name='api_create_topup_order'),  # 建立訂單並紀錄 Log (方案 B)
        path('confirm-payment/', views.api_confirm_payment, name='api_confirm_payment'),  # 驗證支付並增加點數
    ])),
]