from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# LINE Bot SDK 相關
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, TemplateSendMessage, ButtonsTemplate, URITemplateAction
)

# 匯入專案中的模型
from allauth.socialaccount.models import SocialAccount
from coast_guard_mart.models import MemberCredit, CreditTransaction

# 初始化 LINE Bot API 與 Handler
# 直接引用 settings 中的設定
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


# --- 1. 一般網頁 View ---

def add_friend(request):
    """回傳引導使用者加入好友的頁面"""
    return render(request, 'playground/line_bot/add_friend.html')


# --- 2. Webhook 入口 ---

@csrf_exempt
def line_webhook(request):
    """主要 Webhook 入口，處理來自 LINE 的 POST 請求"""
    if request.method == 'POST':
        signature = request.META.get('HTTP_X_LINE_SIGNATURE', '')
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden("Invalid signature.")
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {e}")

        return HttpResponse('OK')

    return HttpResponse("Method Not Allowed", status=405)


# --- 3. LINE 事件處理邏輯 ---

@handler.add(FollowEvent)
def handle_follow(event):
    """當使用者「加入好友」或「解除封鎖」時觸發"""
    welcome_text = (
        "您好！歡迎加入 Dot_Website 官方帳號！🎉\n\n"
        "🔔 功能提示：\n"
        "1. 輸入「餘額」：查詢當年度福利金。\n"
        "2. 輸入「訂單」：查看最近消費紀錄。\n\n"
        "⚠️ 請務必先在網站透過「LINE 登入」完成帳號綁定，才能使用查詢功能喔！"
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_text)
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理使用者傳送的文字訊息"""
    user_text = event.message.text.strip()
    line_uid = event.source.user_id

    # 從 settings 讀取基礎網址，確保全局一致
    base_url = getattr(settings, 'LINE_BASE_URL', '')
    reply_content = None  # 用來存放最終要回傳的訊息物件

    # 邏輯 A：餘額查詢
    if user_text in ["餘額", "查詢餘額", "點數"]:
        social_acc = SocialAccount.objects.filter(provider='line', uid=line_uid).first()
        if social_acc:
            user = social_acc.user
            current_year = timezone.now().year
            credit = MemberCredit.objects.filter(user=user, fiscal_year=current_year, is_active=True).first()
            if credit:
                reply_content = TextSendMessage(
                    text=f"💰 {user.username} 您好：\n您 {current_year} 年度的剩餘點數為 {int(credit.balance)} 元。")
            else:
                reply_content = TextSendMessage(
                    text=f"您好 {user.username}，目前找不到您在 {current_year} 年度的有效點數卡。")
        else:
            reply_content = TextSendMessage(text="⚠️ 系統查無您的綁定資訊。\n請先至網站使用 LINE 登入完成帳號連結。")

    # 邏輯 B：訂單查詢 (使用 ButtonsTemplate)
    elif user_text in ["訂單", "訂單查詢"]:
        social_acc = SocialAccount.objects.filter(provider='line', uid=line_uid).first()
        if social_acc:
            last_tx = CreditTransaction.objects.filter(credit_card__user=social_acc.user).order_by('-timestamp').first()
            if last_tx:
                # 建立按鈕選單，使用拼接後的完整網址
                reply_content = TemplateSendMessage(
                    alt_text='您的訂單狀態',
                    template=ButtonsTemplate(
                        title='訂單狀態查詢',
                        text=f'最末筆訂單：{last_tx.order_id}\n狀態：{last_tx.get_status_display()}',
                        actions=[
                            URITemplateAction(
                                label='查看該訂單詳情',
                                uri=f'{base_url}/coast_guard_mart/order/{last_tx.order_id}/'
                            ),
                            URITemplateAction(
                                label='查看所有訂單',
                                uri=f'{base_url}/coast_guard_mart/my-orders/'
                            )
                        ]
                    )
                )
            else:
                reply_content = TextSendMessage(text=f"您目前沒有消費紀錄。\n商城首頁：{base_url}/coast_guard_mart/")
        else:
            reply_content = TextSendMessage(text="⚠️ 請先至網站完成 LINE 登入綁定帳號。")

    # 邏輯 C：客服
    elif user_text == "客服":
        reply_content = TextSendMessage(text="客服在線時間：週一至週五 09:00-18:00。\n請在此留下您的問題，專人將盡快回覆。")

    # 邏輯 D：其他/預設回覆
    else:
        reply_content = TextSendMessage(text=f"收到訊息：『{user_text}』\n您可以嘗試輸入「餘額」或「訂單」來查詢相關資訊。")

    # 統一回覆出口：一個 reply_token 只能呼叫一次
    if reply_content:
        line_bot_api.reply_message(event.reply_token, reply_content)