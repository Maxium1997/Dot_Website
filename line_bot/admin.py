from django.contrib import admin

# Register your models here.
from .models import UserInfo


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'pic_url', 'message_text', 'message_created_dt')

