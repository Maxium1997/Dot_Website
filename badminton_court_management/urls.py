from django.urls import path, include
from . import views

app_name = 'badminton_court_management'

urlpatterns = [
    path('booking/', views.booking_page, name='booking_page'),

    path('api/', include([
        path('get-gyms/', views.api_get_gyms, name='api_get_gyms'),
        path('get-slots/', views.api_get_slots, name='api_get_slots'),
        path('get-user-balance/', views.api_get_user_balance, name='api_get_user_balance'),
        path('create-booking/', views.api_create_booking, name='api_create_booking'),
        path('get-slots/', views.api_get_slots, name='api_get_slots'),
        path('create-booking/', views.api_create_booking, name='api_create_booking'),
    ])),
]