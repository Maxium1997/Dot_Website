import json
import pytz
from datetime import datetime, time
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount
from linebot import LineBotApi
from linebot.models import FlexSendMessage

from .models import Court, Gym, MemberWallet, Booking
from .utils import get_booking_flex_message
from .services import reserve_court, get_available_slots

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

TAIPEI_TZ = pytz.timezone('Asia/Taipei')


def booking_page(request):
    """渲染預約網頁"""
    now_taipei = timezone.now().astimezone(TAIPEI_TZ)
    context = {
        'today_date': now_taipei.date().isoformat(),
        'liff_id': settings.LINE_LIFF_ID,
    }
    return render(request, 'badminton_court_management/booking.html', context)


def api_get_gyms(request):
    """獲取球館清單 (修正點：加入 try-except 避免 500)"""
    try:
        # 確保你的 Gym 模型欄位名稱正確
        gyms = Gym.objects.all().values('id', 'name', 'address')
        return JsonResponse(list(gyms), safe=False)
    except Exception as e:
        print(f"Error in api_get_gyms: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def api_get_slots(request):
    """獲取時段 (修正點：處理日期解析)"""
    date_str = request.GET.get('date')
    gym_id = request.GET.get('gym_id')
    if not date_str or not gym_id:
        return JsonResponse({"error": "缺少參數"}, status=400)
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        slots_data = get_available_slots(target_date, gym_id=gym_id)
        return JsonResponse(slots_data)
    except Exception as e:
        print(f"Error in api_get_slots: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def api_get_user_balance(request):
    """取得使用者在特定球館的專屬點數"""
    gym_id = request.GET.get('gym_id')
    if not request.user.is_authenticated or not gym_id:
        return JsonResponse({'points': 0})

    wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym_id=gym_id)
    return JsonResponse({'points': wallet.points})


# --- 3. 預約執行 API ---

@csrf_exempt
def api_create_booking(request):
    """API: 執行預約動作並觸發通知"""
    if request.method != "POST":
        return JsonResponse({"status": "error", "msg": "不支援的請求方法"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "msg": "請先登入帳號"}, status=403)

    try:
        data = json.loads(request.body)
        court_name = data.get('court_name')
        date_str = data.get('date')
        start_time_str = data.get('start_time')
        gym_id = data.get('gym_id')

        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        # 處理跨午夜 24:00 邏輯：23:00 的結束時間為 00:00 (隔天)
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
            return JsonResponse({"status": "success", "msg": "預約成功！"})
        else:
            return JsonResponse({"status": "error", "msg": result})

    except Court.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "找不到該場地"})
    except Exception as e:
        return JsonResponse({"status": "error", "msg": f"系統錯誤: {str(e)}"}, status=500)


def send_booking_success_notification(user, booking):
    """預約成功後推播電子憑證"""
    social_acc = SocialAccount.objects.filter(user=user, provider='line').first()
    if social_acc:
        try:
            flex_content = get_booking_flex_message(booking)
            flex_message = FlexSendMessage(
                alt_text=f"🏸 預約成功：{booking.court.gym.name}",
                contents=flex_content
            )
            line_bot_api.push_message(social_acc.uid, flex_message)
        except Exception as e:
            print(f"Push Error: {e}")