from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from .models import UserInfo

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        message = []

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            # 如果事件為訊息
            if isinstance(event, MessageEvent):
                print(event.message.type)
                if event.message.type == 'text':
                    message.append(TextSendMessage(text='文字訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'image':
                    message.append(TextSendMessage(text='圖片訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'location':
                    message.append(TextSendMessage(text='位置訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'video':
                    message.append(TextSendMessage(text='影片訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif event.message.type == 'file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token, message)
                # 如果事件為非訊息
                elif isinstance(event, FollowEvent):
                    print('加入好友')
                    message.append(TextSendMessage(text='歡迎使用沒什麼功能的我'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif isinstance(event, UnfollowEvent):
                    print('取消好友')

                elif isinstance(event, JoinEvent):
                    print('進入群組')
                    message.append(TextSendMessage(text='有人進來了'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif isinstance(event, LeaveEvent):
                    print('離開群組')
                    message.append(TextSendMessage(text='有人出去了'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif isinstance(event, MemberJoinedEvent):
                    print('有人入群')
                    message.append(TextSendMessage(text='有人進來了'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif isinstance(event, MemberLeftEvent):
                    print('有人退群')
                    message.append(TextSendMessage(text='有人出去了'))
                    line_bot_api.reply_message(event.reply_token, message)

                elif isinstance(event, PostbackEvent):
                    print('PostbackEvent')

        for event in events:
            if isinstance(event, MessageEvent):
                message_text = event.message.text
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                name = profile.display_name
                pic_url = profile.picture_url

                try:
                    user = get_object_or_404(UserInfo, uid=uid)
                    message.append(TextSendMessage(text='已經有建立會員資料囉'))
                    info = 'UID=%s\nNAME=%s\n大頭貼=%s' % (user.uid, user.name, user.pic_url)
                    message.append(TextSendMessage(text=info))
                except ObjectDoesNotExist:
                    UserInfo.objects.create(uid=uid, name=name, pic_url=pic_url, message_text=message_text)
                    message.append(TextSendMessage(text='會員資料新增完畢'))

                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def add_friend(request):
    return render(request, 'playground/line_bot/add_friend.html')
