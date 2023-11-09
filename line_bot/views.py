from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)

logger = logging.getLogger("django")

# Create your views here.


@csrf_exempt
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.headers["X-Line-Signature"]

        # get request body as text
        body = request.body.decode()
        # logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            return HttpResponseBadRequest()

        return HttpResponse("OK")

    else:
        return HttpResponseBadRequest()


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(text=event.message.text),
    )
