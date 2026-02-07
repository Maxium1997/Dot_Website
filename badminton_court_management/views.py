import json
import pytz
import uuid
import traceback
from django.db import transaction, models
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth import login

# Allauth 與 LINE 相關整合
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.providers.line.views import LineOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

from Dot_Website.utils import send_line_notification

from linebot import LineBotApi

from .models import Court, Gym, MemberWallet, Booking
from .models import TopupPlan, TopupOrder, TopupOrderLog, PointLog, GymStaff
from .services import reserve_court, get_available_slots
from .services import cancel_booking_as_staff
import qrcode
from io import BytesIO
from .decorators import require_active_gym_staff

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
TAIPEI_TZ = pytz.timezone('Asia/Taipei')


# --- 頁面渲染 ---

def booking_page(request):
    """渲染預約網頁"""
    now_taipei = timezone.now().astimezone(TAIPEI_TZ)
    user_profile_img = ""
    can_view_dashboard = False
    if request.user.is_authenticated:
        social_acc = SocialAccount.objects.filter(user=request.user, provider='line').first()
        if social_acc:
            user_profile_img = social_acc.extra_data.get('pictureUrl') or social_acc.extra_data.get('picture_url')
        can_view_dashboard = GymStaff.objects.filter(user=request.user, is_active=True).exists()

    gyms = Gym.objects.all().order_by('name')
    context = {
        'today_date': now_taipei.date().isoformat(),
        'liff_id': settings.LINE_LIFF_ID,
        'user_profile_img': user_profile_img,
        'gyms': gyms,
        'can_view_dashboard': can_view_dashboard,
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


@login_required
def api_get_user_balance(request):
    """取得點數（整合 LINE 登入後 request.user 就會有資料）"""
    gym_id = request.GET.get('gym_id')
    if not request.user.is_authenticated or not gym_id:
        return JsonResponse({'points': 0, 'authenticated': False})

    wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym_id=gym_id)
    return JsonResponse({'points': wallet.points, 'authenticated': True})


@login_required
def api_create_booking(request):
    if not request.user.is_authenticated:
        messages.error(request, "請先登入後繼續後續動作")
        redirect(reverse('login'))

    """執行預約動作"""
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
            messages.success(request, "預約完成！")

            msg = (
                "✅ 預約成功！\n"
                    f"球館：{result.court.gym.name}\n"
                    f"場地：{result.court}\n"
                    f"日期：{result.booking_date}\n"
                    f"時間：{result.start_time.strftime('%H:%M')} - {result.end_time.strftime('%H:%M')}"
            )
            
            '"透過 LINE 發送預約成功訊息"'
            send_line_notification(request.user, msg)

            return JsonResponse({"status": "success", "msg": "預約成功！"})
        else:
            return JsonResponse({"status": "error", "msg": result})

    except Court.DoesNotExist:
        return JsonResponse({"status": "error", "msg": "場地不存在"}, status=404)
    except Exception as e:
        print(f"Booking Error: {traceback.format_exc()}")
        return JsonResponse({"status": "error", "msg": "系統預約失敗"}, status=500)


@login_required
def topup_page(request):
    gym_id = request.GET.get('gym_id')
    gym = None
    if gym_id:
        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            gym = None
    if gym is None:
        gym = Gym.objects.first()
    now = timezone.now()
    TopupPlan.objects.filter(
        gym=gym,
        is_active=True,
        active_end__isnull=False,
        active_end__lt=now,
        deactivated_at__isnull=True,
    ).update(is_active=False, deactivated_at=now)
    plans = TopupPlan.objects.filter(
        gym=gym,
        is_active=True
    ).filter(
        models.Q(active_start__isnull=True) | models.Q(active_start__lte=now)
    ).filter(
        models.Q(active_end__isnull=True) | models.Q(active_end__gte=now)
    ).order_by('amount')
    wallet, _ = MemberWallet.objects.get_or_create(user=request.user, gym=gym)
    can_manage_plans = False
    if request.user.is_authenticated:
        role = _get_user_role_for_gym(request.user, gym)
        can_manage_plans = role in [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER]

    return render(request, 'badminton_court_management/topup.html', {
        'gym': gym,
        'plans': plans,
        'wallet': wallet,
        'can_manage_plans': can_manage_plans,
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
        now = timezone.now()
        TopupPlan.objects.filter(
            gym_id=gym_id,
            is_active=True,
            active_end__isnull=False,
            active_end__lt=now,
            deactivated_at__isnull=True,
        ).update(is_active=False, deactivated_at=now)
        plan = TopupPlan.objects.filter(
            id=plan_id,
            gym_id=gym_id,
            is_active=True
        ).filter(
            models.Q(active_start__isnull=True) | models.Q(active_start__lte=now)
        ).filter(
            models.Q(active_end__isnull=True) | models.Q(active_end__gte=now)
        ).first()
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

        _send_topup_pending_notification(request, order)
        return JsonResponse({
            'status': 'success',
            'order_id': order.order_id,
            'amount': order.amount,
            'msg': '訂單已建立，請至櫃台完成核銷。'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': "訂單建立失敗"}, status=500)


def _is_staff(user):
    return user.is_staff


def _get_active_gym_roles(user):
    return GymStaff.objects.select_related('gym').filter(user=user, is_active=True)


def _get_selected_gym(request, gyms_qs):
    gym_id = request.GET.get('gym_id')
    if gym_id:
        try:
            return gyms_qs.get(gym_id=int(gym_id))
        except (GymStaff.DoesNotExist, ValueError):
            return gyms_qs.first()
    return gyms_qs.first()


def _get_user_role_for_gym(user, gym):
    role_obj = GymStaff.objects.filter(user=user, gym=gym, is_active=True).first()
    return role_obj.role if role_obj else None


def _require_role(user, gym, allowed_roles):
    role = _get_user_role_for_gym(user, gym)
    if role not in allowed_roles:
        raise PermissionDenied
    return role


def _dashboard_redirect(gym):
    return redirect(f"{reverse('badminton_court_management:staff_gym_dashboard')}?gym_id={gym.id}")


def _send_topup_pending_notification(request, order):
    base_url = getattr(settings, 'LINE_BASE_URL', '').rstrip('/')
    path = reverse('badminton_court_management:topup_order_qrcode', args=[order.order_id])
    qr_url = f"{base_url}{path}" if base_url else request.build_absolute_uri(path)
    message_text = (
        "✅ 儲值訂單已建立\n"
        f"訂單編號：{order.order_id}\n"
        f"球館：{order.wallet.gym.name}\n"
        f"方案：{order.plan.name if order.plan else '-'}\n"
        f"金額：NT$ {order.amount}\n"
        "請出示以下 QR Code 至櫃台核銷：\n"
        f"{qr_url}"
    )
    send_line_notification(order.user, message_text)


@login_required
@require_active_gym_staff
def staff_gym_dashboard(request):
    gyms_qs = _get_active_gym_roles(request.user)
    if not gyms_qs.exists():
        raise PermissionDenied

    selected_role = None
    selected_gym_role = _get_selected_gym(request, gyms_qs)
    if selected_gym_role:
        selected_role = selected_gym_role.role
        selected_gym = selected_gym_role.gym
    else:
        raise PermissionDenied

    bookings = Booking.objects.select_related('court', 'court__gym', 'user') \
        .filter(court__gym=selected_gym) \
        .order_by('-booking_date', '-start_time')

    orders = TopupOrder.objects.select_related('user', 'wallet__gym', 'plan') \
        .filter(wallet__gym=selected_gym) \
        .order_by('-created_at')

    return render(request, 'badminton_court_management/staff/dashboard.html', {
        'gym_roles': gyms_qs,
        'selected_gym_role': selected_gym_role,
        'selected_gym': selected_gym,
        'selected_role': selected_role,
        'bookings': bookings,
        'orders': orders,
    })


@login_required
@require_active_gym_staff
@transaction.atomic
def staff_topup_approve(request, order_id):
    if request.method != 'POST':
        raise PermissionDenied

    try:
        order = TopupOrder.objects.select_for_update().select_related('wallet__gym').get(order_id=order_id)
        _require_role(request.user, order.wallet.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER, GymStaff.ROLE_CLERK])

        if order.status == 'success':
            messages.info(request, "訂單已完成。")
            return _dashboard_redirect(order.wallet.gym)
        if order.status in ['failed', 'cancelled']:
            messages.warning(request, "訂單已結束，無法核銷。")
            return _dashboard_redirect(order.wallet.gym)

        old_status = order.status
        order.status = 'success'
        order.paid_at = timezone.now()
        order.save()

        wallet = order.wallet
        wallet.points += order.points
        wallet.save()

        TopupOrderLog.objects.create(
            order=order,
            from_status=old_status,
            to_status='success',
            operator=request.user.username,
            remark="櫃台核銷成功"
        )
        PointLog.objects.create(wallet=wallet, amount=order.points, reason=f"儲值核銷成功: {order.order_id}")
        messages.success(request, f"訂單 {order.order_id} 已核銷。")
        return _dashboard_redirect(order.wallet.gym)
    except TopupOrder.DoesNotExist:
        messages.error(request, "找不到該訂單。")
        return redirect('badminton_court_management:staff_gym_dashboard')


@login_required
@require_active_gym_staff
@transaction.atomic
def staff_topup_reject(request, order_id):
    if request.method != 'POST':
        raise PermissionDenied

    try:
        order = TopupOrder.objects.select_for_update().select_related('wallet__gym').get(order_id=order_id)
        _require_role(request.user, order.wallet.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER])

        if order.status == 'success':
            messages.warning(request, "訂單已完成，無法取消。")
            return _dashboard_redirect(order.wallet.gym)
        if order.status in ['failed', 'cancelled']:
            messages.info(request, "訂單已結束。")
            return _dashboard_redirect(order.wallet.gym)

        old_status = order.status
        order.status = 'cancelled'
        order.save()

        TopupOrderLog.objects.create(
            order=order,
            from_status=old_status,
            to_status='cancelled',
            operator=request.user.username,
            remark="櫃台取消訂單"
        )
        messages.success(request, f"訂單 {order.order_id} 已取消。")
        return _dashboard_redirect(order.wallet.gym)
    except TopupOrder.DoesNotExist:
        messages.error(request, "找不到該訂單。")
        return redirect('badminton_court_management:staff_gym_dashboard')


@login_required
@require_active_gym_staff
@transaction.atomic
def staff_booking_cancel(request, booking_id):
    if request.method != 'POST':
        raise PermissionDenied

    try:
        booking = Booking.objects.select_for_update().select_related('court__gym').get(id=booking_id)
        _require_role(request.user, booking.court.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER])
        ok, msg = cancel_booking_as_staff(booking)
        if ok:
            messages.success(request, "預約已取消。")
        else:
            messages.warning(request, msg)
        return _dashboard_redirect(booking.court.gym)
    except Booking.DoesNotExist:
        messages.error(request, "找不到預約紀錄。")
        return redirect('badminton_court_management:staff_gym_dashboard')


@login_required
@require_active_gym_staff
def staff_gym_staff(request):
    gyms_qs = _get_active_gym_roles(request.user)
    if not gyms_qs.exists():
        raise PermissionDenied

    selected_gym_role = _get_selected_gym(request, gyms_qs)
    if not selected_gym_role:
        raise PermissionDenied

    _require_role(request.user, selected_gym_role.gym, [GymStaff.ROLE_ADMIN])

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            username = request.POST.get('username', '').strip()
            role = request.POST.get('role', GymStaff.ROLE_CLERK)
            if not username:
                messages.error(request, "請輸入使用者帳號。")
            else:
                user = get_user_model().objects.filter(username=username).first()
                if not user:
                    messages.error(request, "找不到使用者。")
                else:
                    GymStaff.objects.update_or_create(
                        user=user,
                        gym=selected_gym_role.gym,
                        defaults={'role': role, 'is_active': True}
                    )
                    messages.success(request, f"{username} 權限已更新。")
            return redirect(f"{reverse('badminton_court_management:staff_gym_staff')}?gym_id={selected_gym_role.gym.id}")
        if action == 'update':
            staff_id = request.POST.get('staff_id')
            role = request.POST.get('role', GymStaff.ROLE_CLERK)
            is_active = request.POST.get('is_active') == 'on'
            staff = GymStaff.objects.filter(id=staff_id, gym=selected_gym_role.gym).first()
            if staff:
                staff.role = role
                staff.is_active = is_active
                staff.save(update_fields=['role', 'is_active', 'updated_at'])
                messages.success(request, "權限已更新。")
            return redirect(f"{reverse('badminton_court_management:staff_gym_staff')}?gym_id={selected_gym_role.gym.id}")

    staff_list = GymStaff.objects.select_related('user') \
        .filter(gym=selected_gym_role.gym) \
        .order_by('role', 'user__username')

    return render(request, 'badminton_court_management/staff/gym_staff.html', {
        'gym_roles': gyms_qs,
        'selected_gym_role': selected_gym_role,
        'selected_gym': selected_gym_role.gym,
        'staff_list': staff_list,
    })


@login_required
@require_active_gym_staff
def staff_topup_verify(request, order_id):
    order = TopupOrder.objects.select_related('wallet__gym', 'plan', 'user').filter(order_id=order_id).first()
    if not order:
        messages.error(request, "找不到該訂單。")
        return redirect('badminton_court_management:staff_gym_dashboard')

    _require_role(request.user, order.wallet.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER, GymStaff.ROLE_CLERK])
    return render(request, 'badminton_court_management/staff/topup_verify.html', {'order': order})


@login_required
@require_active_gym_staff
def staff_topup_plans(request):
    gyms_qs = _get_active_gym_roles(request.user)
    if not gyms_qs.exists():
        raise PermissionDenied

    selected_gym_role = _get_selected_gym(request, gyms_qs)
    if not selected_gym_role:
        raise PermissionDenied

    _require_role(request.user, selected_gym_role.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER])

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        amount = request.POST.get('amount', '').strip()
        points = request.POST.get('points', '').strip()
        is_recommended = request.POST.get('is_recommended') == 'on'
        active_start = request.POST.get('active_start', '').strip()
        active_end = request.POST.get('active_end', '').strip()

        if not name or not amount.isdigit() or not points.isdigit():
            messages.error(request, "請填寫正確的方案名稱、金額與點數。")
        else:
            start_dt = None
            end_dt = None
            try:
                if active_start:
                    start_dt = datetime.fromisoformat(active_start)
                if active_end:
                    end_dt = datetime.fromisoformat(active_end)
            except ValueError:
                messages.error(request, "活動時間格式錯誤。")
                return redirect(f"{reverse('badminton_court_management:staff_topup_plans')}?gym_id={selected_gym_role.gym.id}")

            if start_dt and timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt)
            if end_dt and timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt)

            TopupPlan.objects.create(
                gym=selected_gym_role.gym,
                name=name,
                amount=int(amount),
                points=int(points),
                is_active=True,
                is_recommended=is_recommended,
                active_start=start_dt,
                active_end=end_dt,
            )
            messages.success(request, "儲值方案已建立。")
        return redirect(f"{reverse('badminton_court_management:staff_topup_plans')}?gym_id={selected_gym_role.gym.id}")

    now = timezone.now()
    TopupPlan.objects.filter(
        gym=selected_gym_role.gym,
        is_active=True,
        active_end__isnull=False,
        active_end__lt=now,
        deactivated_at__isnull=True,
    ).update(is_active=False, deactivated_at=now)
    plans = TopupPlan.objects.filter(gym=selected_gym_role.gym).annotate(
        purchase_count=Count('topuporder', filter=Q(topuporder__status='success'))
    ).order_by('-is_active', 'amount')
    return render(request, 'badminton_court_management/staff/topup_plans.html', {
        'gym_roles': gyms_qs,
        'selected_gym_role': selected_gym_role,
        'selected_gym': selected_gym_role.gym,
        'plans': plans,
    })


@login_required
@require_active_gym_staff
@transaction.atomic
def staff_topup_plan_deactivate(request, plan_id):
    if request.method != 'POST':
        raise PermissionDenied

    plan = TopupPlan.objects.select_for_update().select_related('gym').filter(id=plan_id).first()
    if not plan:
        messages.error(request, "找不到方案。")
        return redirect('badminton_court_management:staff_gym_dashboard')

    _require_role(request.user, plan.gym, [GymStaff.ROLE_ADMIN, GymStaff.ROLE_MANAGER])
    if plan.is_active:
        now = timezone.now()
        plan.is_active = False
        if plan.deactivated_at is None:
            plan.deactivated_at = now
        plan.save(update_fields=['is_active', 'deactivated_at'])
        messages.success(request, "方案已停用。")
    else:
        messages.info(request, "方案已停用。")

    return redirect(f"{reverse('badminton_court_management:staff_topup_plans')}?gym_id={plan.gym.id}")


def topup_order_qrcode(request, order_id):
    order = TopupOrder.objects.select_related('wallet__gym').filter(order_id=order_id).first()
    if not order:
        return JsonResponse({'error': '訂單不存在'}, status=404)

    base_url = getattr(settings, 'LINE_BASE_URL', '').rstrip('/')
    path = reverse('badminton_court_management:staff_topup_verify', args=[order.order_id])
    verify_url = f"{base_url}{path}" if base_url else request.build_absolute_uri(path)

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(verify_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
