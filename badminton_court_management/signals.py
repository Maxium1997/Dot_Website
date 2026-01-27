from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from allauth.socialaccount.signals import social_account_added
from linebot import LineBotApi
from linebot.models import TextSendMessage
from .models import MemberWallet, PointLog

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_wallet(sender, instance, created, **kwargs):
    """當 User 建立時同步建立錢包，更新時同步儲存"""
    if created:
        MemberWallet.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, 'wallet'):
            instance.wallet.save()

@receiver(social_account_added)
def gift_points_and_send_welcome(request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'line':
        user = sociallogin.user
        line_uid = sociallogin.account.uid

        wallet, created = MemberWallet.objects.get_or_create(user=user)
        gift_amount = 50
        wallet.points += gift_amount
        wallet.save()

        PointLog.objects.create(
            wallet=wallet,
            amount=gift_amount,
            reason="LINE 首次綁定獎勵"
        )

        try:
            welcome_msg = (
                f"🎉 恭喜 {user.username} 綁定成功！\n\n"
                f"系統已自動為您存入 {gift_amount} 點開戶禮！🎁\n\n"
                "🏸 您現在可以開始預約場地了：\n"
                "👉 輸入「預約」：開啟預約系統\n"
                "👉 輸入「查詢點數」：查看餘額"
            )
            line_bot_api.push_message(line_uid, TextSendMessage(text=welcome_msg))
        except Exception as e:
            print(f"LINE Push Message Error: {e}")