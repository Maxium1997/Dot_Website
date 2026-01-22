from linebot import LineBotApi
from linebot.models import TextSendMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def send_line_notification(user, message_text):
    """
    發送 LINE 訊息給使用者。
    前提：使用者必須是透過 LINE 登入，且 socialaccount 中存有其 uid。
    """
    # 透過 django-allauth 取得該使用者的 LINE UID
    social_acc = user.socialaccount_set.filter(provider='line').first()

    if not social_acc:
        logger.warning(f"使用者 {user.username} 沒有關聯的 LINE 帳號，無法發送通知。")
        return False

    line_user_id = social_acc.uid  # allauth 將 LINE 的內部 ID 存於 uid 欄位

    try:
        line_bot_api.push_message(line_user_id, TextSendMessage(text=message_text))
        return True
    except Exception as e:
        logger.error(f"LINE 訊息發送至 {user.username} 失敗: {str(e)}")
        return False