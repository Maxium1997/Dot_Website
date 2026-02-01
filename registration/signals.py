from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def custom_login_message(sender, request, user, **kwargs):
    # 清除之前的預設訊息 (選擇性)
    storage = messages.get_messages(request)
    storage.used = True

    # 取得要顯示的名稱
    display_name = user.first_name if user.first_name else "使用者"

    # 發送自定義的訊息
    messages.info(request, f"您已成功登入為 {display_name}。")
