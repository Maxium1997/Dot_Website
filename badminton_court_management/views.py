import json
import pytz
from datetime import datetime, time
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import login

# Allauth 相關整合
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.line.views import LineOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

from linebot import LineBotApi
from linebot.models import FlexSendMessage

from .models import Court, Gym, MemberWallet, Booking
from .utils import get_booking_flex_message
from .services import reserve_court, get_available_slots

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
TAIPEI_TZ = pytz.timezone('Asia/Taipei')


# --- 1. 頁面與基礎 API ---

# badminton_court_management/views.py

def booking_page(request):
    """渲染預約網頁"""
    now_taipei = timezone.now().astimezone(TAIPEI_TZ)

    user_profile_img = ""
    if request.user.is_authenticated:
        # 取得該使用者的 LINE 社交帳號資訊
        social_acc = SocialAccount.objects.filter(user=request.user, provider='line').first()
        if social_acc:
            # LINE 的原始資料儲存在 extra_data 字典中
            # 注意：欄位可能是 pictureUrl 或 picture_url，視 allauth 版本而定
            user_profile_img = social_acc.extra_data.get('pictureUrl') or social_acc.extra_data.get('picture_url')

    context = {
        'today_date': now_taipei.date().isoformat(),
        'liff_id': settings.LINE_LIFF_ID,
        'user_profile_img': user_profile_img,  # 將網址傳給模板
    }
    return render(request, 'badminton_court_management/booking.html', context)


@csrf_exempt # 測試階段可以先加這行，排除 CSRF 疑慮
def api_liff_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    """
    LIFF 登入整合 API：
    接收前端 liff.getAccessToken()，透過 allauth 進行靜默登入。
    這會將 LINE UID 與你自定義的 Member 模型自動關聯。
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        access_token = data.get('access_token')

        if not access_token:
            return JsonResponse({"error": "Missing access token"}, status=400)

        # 使用 Allauth 的 LineAdapter 驗證 token
        adapter = LineOAuth2Adapter(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)

        # 這裡會向 LINE 伺服器驗證 token 並取得 profile
        token = adapter.parse_token({'access_token': access_token})
        login_obj = adapter.complete_login(request, app, token, response=None)
        login_obj.token = token
        login_obj.state = SocialLogin.state_from_request(request)

        # 在執行 complete_social_login 前檢查
        print(f"DEBUG: 正在嘗試登入 LINE User, Token: {access_token[:10]}...")

        ret = complete_social_login(request, login_obj)

        # 如果 complete_social_login 回傳的是 HttpResponseRedirect，代表成功跳轉
        return JsonResponse({"status": "success"})
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 這會在你的終端機印出詳細錯誤
        return JsonResponse({"status": "error", "msg": str(e)}, status=500)

        # complete_social_login 會處理：
        # 1. 如果已有 SocialAccount，則登入關聯的 Member
        # 2. 如果沒有，則根據 settings 建立新的 Member
        complete_social_login(request, login_obj)

        return JsonResponse({
            "status": "success",
            "user": request.user.username,
            "authenticated": request.user.is_authenticated
        })
    except Exception as e:
        print(f"LIFF Login Error: {e}")
        return JsonResponse({"status": "error", "msg": str(e)}, status=500)


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


# --- 2. 預約執行 API ---

@csrf_exempt
def api_create_booking(request):
    """執行預約動作"""
    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "不支援的方法"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "msg": "帳號未識別，請重新開啟頁面"}, status=403)

    try:
        data = json.loads(request.body)
        court_name = data.get('court_name')
        date_str = data.get('date')
        start_time_str = data.get('start_time')
        gym_id = data.get('gym_id')

        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        # 結束時間邏輯
        if start_time.hour == 23:
            end_time = time(0, 0)
        else:
            end_time = time(start_time.hour + 1, start_time.minute)

        court = Court.objects.get(number=court_name, gym_id=gym_id, is_active=True)

        # 執行 Service 邏輯（包含 Transaction 和扣點）
        success, result = reserve_court(
            user=request.user,
            court=court,
            booking_date=target_date,
            start_time=start_time,
            end_time=end_time
        )

        if success:
            send_booking_success_notification(request.user, result)
            return JsonResponse({"status": "success", "msg": "預約成功！"})
        else:
            return JsonResponse({"status": "error", "msg": result})

    except Court.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "找不到該場地"})
    except Exception as e:
        return JsonResponse({"status": "error", "msg": f"系統錯誤: {str(e)}"}, status=500)


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
            line_bot_api.push_message(social_acc.uid, flex_message)
        except Exception as e:
            print(f"LINE Push Error: {e}")