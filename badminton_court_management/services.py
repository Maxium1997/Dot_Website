from django.db import transaction
from django.utils import timezone
from .models import Booking, PointLog, MemberWallet, Court
from datetime import time, datetime

import pytz


def reserve_court(user, court, booking_date, start_time, end_time):
    # 0. 額外安全檢查：不允許預約過去的時間
    tz = pytz.timezone('Asia/Taipei')
    now_taipei = timezone.now().astimezone(tz)
    # 將預約日期與時間合併成 datetime 物件進行比較
    target_dt = tz.localize(datetime.combine(booking_date, start_time))
    if target_dt < now_taipei:
        return False, "無法預約過去的時段。"
    """
    執行預約服務：按球館定位錢包 -> 檢查衝突 -> 扣點 -> 建立預約
    """
    target_gym = court.gym

    # 1. 檢查時段衝突
    is_conflict = Booking.objects.filter(
        court=court,
        booking_date=booking_date,
        start_time=start_time,
        status='confirmed'
    ).exists()

    if is_conflict:
        return False, "該時段已被他人預約。"

    # 2. 獲取錢包
    wallet, created = MemberWallet.objects.get_or_create(user=user, gym=target_gym)

    # 3. 檢查點數
    price = court.price_per_hour
    if wallet.points < price:
        return False, f"您在 {target_gym.name} 的點數不足，剩餘 {wallet.points}。"

    try:
        with transaction.atomic():
            # 2. 鎖定錢包並獲取最新餘額
            wallet, _ = MemberWallet.objects.select_for_update().get_or_create(
                user=user, gym=court.gym
            )

            price = court.price_per_hour
            if wallet.points < price:
                return False, f"點數不足，剩餘 {wallet.points}。"

            # 扣點
            wallet.points -= price
            wallet.save()

            # 記錄流水
            PointLog.objects.create(
                wallet=wallet,
                amount=-price,
                reason=f"預約場地：{court.number} ({booking_date} {start_time})"
            )

            # 建立預約
            booking = Booking.objects.create(
                user=user,
                court=court,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                total_points=price,
                status='confirmed'
            )
        return True, booking
    except Exception as e:
        return False, f"預約失敗：{str(e)}"


def get_available_slots(target_date, gym_id=None):
    tz = pytz.timezone('Asia/Taipei')
    now_taipei = timezone.now().astimezone(tz)
    current_date = now_taipei.date()
    current_hour = now_taipei.hour

    query_filter = {'is_active': True}
    if gym_id:
        query_filter['gym_id'] = gym_id

    courts = Court.objects.filter(**query_filter)
    results = {}

    for court in courts:
        slots = []
        booked_times = Booking.objects.filter(
            court=court,
            booking_date=target_date,
            status='confirmed'
        ).values_list('start_time', flat=True)

        for hour in range(9, 24):
            # 如果是今天且小時已過，則跳過
            if target_date == current_date and hour <= current_hour:
                continue
            if target_date < current_date:
                continue

            start_t = time(hour, 0)
            slots.append({
                'time': f"{hour:02d}:00",
                'is_available': start_t not in booked_times
            })
        results[str(court.number)] = slots
    return results


@transaction.atomic
def cancel_booking(user, booking_id):
    """
    取消預約並將點數退回原球館錢包
    """
    try:
        booking = Booking.objects.select_for_update().select_related('court__gym').get(
            id=booking_id, user=user
        )

        if booking.status != 'confirmed':
            return False, "該預約已取消或無法更改。"

        gym = booking.court.gym
        wallet = MemberWallet.objects.select_for_update().get(user=user, gym=gym)
        refund_amount = booking.total_points

        wallet.points += refund_amount
        wallet.save()

        PointLog.objects.create(
            wallet=wallet,
            amount=refund_amount,
            reason=f"取消預約退費: {booking.court.number} ({booking.booking_date})"
        )

        booking.status = 'cancelled'
        booking.save()

        return True, "預約已取消，點數已退還。"
    except Booking.DoesNotExist:
        return False, "找不到預約紀錄。"
    except Exception as e:
        return False, f"取消失敗: {str(e)}"