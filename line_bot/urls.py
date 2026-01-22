from django.urls import path
from . import views

app_name = 'line_bot'

urlpatterns = [
    # 建議將 callback 改為與 LINE Console 設定一致的路徑
    path('callback', views.line_webhook, name='callback'),
    path('add_friend', views.add_friend, name='line_bot_add_friend'),
]