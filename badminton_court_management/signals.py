from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from allauth.socialaccount.signals import social_account_added
from linebot import LineBotApi
from linebot.models import TextSendMessage
from .models import MemberWallet, PointLog

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


# --- 1. 移除或註解掉 create_or_save_user_wallet ---
# 理由：錢包必須關聯 gym_id，全域建立會導致 IntegrityError
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_or_save_user_wallet(sender, instance, created, **kwargs):
#     pass

# --- 2. 修正贈分邏輯 ---
@receiver(social_account_added)
def gift_points_and_send_welcome(request, sociallogin, **kwargs):
    """
    當使用者綁定 LINE 時觸發。
    注意：這裡我們暫時不在此處建立 MemberWallet，因為不知道 gym_id。
    改為發送歡迎訊息，等使用者進入預約頁面選定球館後，再由 View 建立錢包。
    """
    if sociallogin.account.provider == 'line':
        user = sociallogin.user
        line_uid = sociallogin.account.uid

        # 這裡的邏輯可以改為存入一個「待領取點數表」
        # 或者直接發送歡迎語。若要給點數，必須先確定是給哪一間球館。

        try:
            welcome_msg = (
                f"🎉 恭喜綁定成功！\n\n"
                f"🏸 歡迎使用羽球預約系統！\n\n"
                "👉 輸入「預約」：開啟系統並領取新會員點數\n"
                "👉 輸入「查詢」：查看您的最新動態"
            )
            line_bot_api.push_message(line_uid, TextSendMessage(text=welcome_msg))
        except Exception as e:
            print(f"LINE Push Message Error: {e}")