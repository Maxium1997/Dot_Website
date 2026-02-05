import json
import pytz
import uuid
import traceback
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth import login

# Allauth 與 LINE 相關整合
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.line.views import LineOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

from linebot import LineBotApi
from linebot.models import FlexSendMessage, TextSendMessage

from .models import Court, Gym, MemberWallet, Booking
from .models import TopupPlan, TopupOrder, TopupOrderLog, PointLog
from .utils import get_booking_flex_message
from .services import reserve_court, get_available_slots

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
TAIPEI_TZ = pytz.timezone('Asia/Taipei')


# --- 頁面渲染 ---

def booking_page(request):
    """渲染預約網頁"""
    now_taipei = timezone.now().astimezone(TAIPEI_TZ)
    user_profile_img = ""
    if request.user.is_authenticated:
        social_acc = SocialAccount.objects.filter(user=request.user, provider='line').first()
        if social_acc:
            user_profile_img = social_acc.extra_data.get('pictureUrl') or social_acc.extra_data.get('picture_url')

    gyms = Gym.objects.all().order_by('name')
    context = {
        'today_date': now_taipei.date().isoformat(),
        'liff_id': settings.LINE_LIFF_ID,
        'user_profile_img': user_profile_img,
        'gyms': gyms,
    }
    return render(request, 'badminton_court_management/booking.html', context)


# --- 安全強化後的 API ---

def api_liff_login(request):
    """
    LIFF 登入 API：
    不再使用 @csrf_exempt。LIFF 前端應在 POST 時帶上 CSRF Token。
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        access_token = data.get('access_token')

        if not access_token:
            return JsonResponse({"error": "Missing access token"}, status=400)

        adapter = LineOAuth2Adapter(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)

        token = adapter.parse_token({'access_token': access_token})
        login_obj = adapter.complete_login(request, app, token, response=None)
        login_obj.token = token
        login_obj.state = SocialLogin.state_from_request(request)

        complete_social_login(request, login_obj)

        return JsonResponse({"status": "success", "user": request.user.username})
    except Exception as e:
        # 資安考量：後端記錄詳細 log，前端回傳模糊訊息
        print(f"Login Error: {traceback.format_exc()}")
        return JsonResponse({"status": "error", "msg": "登入驗證失敗，請重新嘗試"}, status=500)


def api_get_gyms(request):
    """獲取球館清單"""
    try:
        gyms = Gym.objects.all().values('id', 'name', 'address')
        return JsonResponse(list(gyms), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def api_get_slots(request):
    """獲取時段"""
    date_str = request.GET.get('date')
    gym_id = request.GET.get('gym_id')
    if not date_str or not gym_id:
        return JsonResponse({"error": "缺少參數"}, status=400)
    try:
        gym_id = int(gym_id)
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        slots_data = get_available_slots(target_date, gym_id=gym_id)
        return JsonResponse(slots_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def api_get_user_balance(request):
    """取得點數（整合 LINE 登入後 request.user 就會有資料）"""
    gym_id = request.GET.get('gym_id')
    if not request.user.is_authenticated or not gym_id:
        return JsonResponse({'points': 0, 'authenticated': False})

    wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym_id=gym_id)
    return JsonResponse({'points': wallet.points, 'authenticated': True})


@login_required
def api_create_booking(request):
    """執行預約動作（移除 @csrf_exempt）"""
    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "不支援的方法"}, status=405)

    try:
        data = json.loads(request.body)
        court_name = data.get('court_name')
        date_str = data.get('date')
        start_time_str = data.get('start_time')
        gym_id = data.get('gym_id')

        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        if start_time.hour == 23:
            end_time = time(0, 0)
        else:
            end_time = time(start_time.hour + 1, start_time.minute)

        court = Court.objects.get(number=court_name, gym_id=gym_id, is_active=True)

        success, result = reserve_court(
            user=request.user,
            court=court,
            booking_date=target_date,
            start_time=start_time,
            end_time=end_time
        )

        if success:
            send_booking_success_notification(request.user, result)
            messages.success(request, "預約完成！")
            return JsonResponse({"status": "success", "msg": "預約成功！"})
        else:
            return JsonResponse({"status": "error", "msg": result})

    except Court.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "場地不存在"}, status=404)
    except Exception as e:
        print(f"Booking Error: {traceback.format_exc()}")
        return JsonResponse({"status": "error", "msg": "系統預約失敗"}, status=500)


def send_booking_success_notification(user, booking):
    """發送 Flex Message 電子憑證"""
    # 從整合後的 SocialAccount 取得 LINE UID
    social_acc = SocialAccount.objects.filter(user=user, provider='line').first()
    if social_acc:
        try:
            flex_content = get_booking_flex_message(booking)
            flex_message = FlexSendMessage(
                alt_text=f"🏸 預約成功通知",
                contents=flex_content
            )
            text_message = TextSendMessage(
                text=(
                    "✅ 預約成功！\n"
                    f"球館：{booking.court.gym.name}\n"
                    f"場地：{booking.court.number}\n"
                    f"日期：{booking.booking_date}\n"
                    f"時間：{booking.start_time.strftime('%H:%M')} - {booking.end_time.strftime('%H:%M')}"
                )
            )
            line_bot_api.push_message(social_acc.uid, [text_message, flex_message])
        except Exception as e:
            print(f"LINE Push Error: {e}")


def topup_page(request):
    gym = Gym.objects.first()  # 獲取當前球館
    plans = TopupPlan.objects.filter(gym=gym, is_active=True).order_by('amount')
    wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym=gym)

    return render(request, 'badminton_court_management/topup.html', {
        'gym': gym,
        'plans': plans,
        'wallet': wallet
    })


@login_required
@transaction.atomic
def api_create_topup_order(request):
    """第一步：產生 pending 訂單"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': '無效請求'}, status=405)

    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        gym_id = data.get('gym_id')

        # 直接從 DB 取值防止前端竄改金額
        plan = TopupPlan.objects.filter(id=plan_id, gym_id=gym_id, is_active=True).first()
        if not plan:
            return JsonResponse({'status': 'error', 'msg': '無效的儲值方案'})

        wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym_id=gym_id)

        order = TopupOrder.objects.create(
            order_id=f"TOPUP-{uuid.uuid4().hex[:12].upper()}",
            user=request.user,
            wallet=wallet,
            plan=plan,
            amount=plan.amount,
            points=plan.points,
            status='pending'
        )

        TopupOrderLog.objects.create(order=order, from_status='None', to_status='pending', remark="訂單已建立")

        return JsonResponse({'status': 'success', 'order_id': order.order_id, 'amount': order.amount})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': "訂單建立失敗"}, status=500)


@login_required
@transaction.atomic
def api_confirm_payment(request):
    """
    第二步：模擬支付成功。
    注意：未來對接正式金流時，此 API 必須檢驗金流商簽章，不可信任前端請求。
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'msg': '無效請求'}, status=405)

    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')

        # 使用 select_for_update 鎖定行，防止併發操作
        order = TopupOrder.objects.select_for_update().get(order_id=order_id, user=request.user)

        if order.status == 'success':
            return JsonResponse({'status': 'error', 'msg': '請勿重複支付'})

        old_status = order.status
        order.status = 'success'
        order.paid_at = timezone.now()
        order.save()

        wallet = order.wallet
        wallet.points += order.points
        wallet.save()

        TopupOrderLog.objects.create(order=order, from_status=old_status, to_status='success', remark="模擬支付成功")
        PointLog.objects.create(wallet=wallet, amount=order.points, reason=f"儲值成功: {order.order_id}")

        return JsonResponse({'status': 'success', 'new_balance': wallet.points})
    except TopupOrder.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': '找不到該訂單'}, status=404)
