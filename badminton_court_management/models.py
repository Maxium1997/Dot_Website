from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# --- 球館管理 ---
class Gym(models.Model):
    name = models.CharField(max_length=100, verbose_name="球館名稱")
    address = models.TextField(verbose_name="地址")
    phone = models.CharField(max_length=20, verbose_name="聯絡電話")

    def __str__(self):
        return self.name


# --- 球場（場地）管理 ---
class Court(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='courts')
    number = models.CharField(max_length=20, verbose_name="場地編號 (如: A場)")
    is_active = models.BooleanField(default=True, verbose_name="是否開放")
    price_per_hour = models.IntegerField(default=500, verbose_name="每小時點數")

    def __str__(self):
        return f"{self.gym.name} - {self.number}"


# --- 會員點數錢包 (按球館區分) ---
class MemberWallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='wallets'  # 改為複數，因為一個 user 有多個錢包
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.PROTECT,
        related_name='member_wallets'
    )
    points = models.PositiveIntegerField(default=0, verbose_name="可用點數")

    class Meta:
        # 確保「一個使用者」在「一家球館」只有一個錢包紀錄
        unique_together = ('user', 'gym')

    def __str__(self):
        return f"{self.user.username} @ {self.gym.name} ({self.points} pts)"


# --- 球場預約模型 ---
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('confirmed', '預約成功'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    booking_date = models.DateField(verbose_name="預約日期")
    start_time = models.TimeField(verbose_name="開始時間")
    end_time = models.TimeField(verbose_name="結束時間")

    total_points = models.IntegerField(verbose_name="扣除點數")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('court', 'booking_date', 'start_time')

    def __str__(self):
        return f"{self.booking_date} {self.court} ({self.user.username})"


# --- 點數流水帳 ---
class PointLog(models.Model):
    wallet = models.ForeignKey(MemberWallet, on_delete=models.PROTECT, related_name='logs')
    amount = models.IntegerField(verbose_name="變動點數")
    reason = models.CharField(max_length=100, verbose_name="變動原因")
    created_at = models.DateTimeField(auto_now_add=True)


# --- 儲值方案 (由球館管理者定義) ---
class TopupPlan(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name='topup_plans')
    name = models.CharField(max_length=50, verbose_name="方案名稱")
    amount = models.PositiveIntegerField(verbose_name="支付金額 (TWD)")
    points = models.PositiveIntegerField(verbose_name="獲得點數")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    is_recommended = models.BooleanField(default=False, verbose_name="推薦方案")
    active_start = models.DateTimeField(null=True, blank=True, verbose_name="活動開始時間")
    active_end = models.DateTimeField(null=True, blank=True, verbose_name="活動結束時間")
    deactivated_at = models.DateTimeField(null=True, blank=True, verbose_name="失效時間")

    def __str__(self):
        return f"{self.gym.name} - {self.name} (${self.amount})"


# --- 儲值訂單 (主表) ---
class TopupOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('processing', '支付中'),
        ('success', '儲值成功'),
        ('failed', '儲值失敗'),
        ('cancelled', '已取消'),
    ]

    order_id = models.CharField(max_length=50, unique=True, verbose_name="訂單編號")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    wallet = models.ForeignKey(MemberWallet, on_delete=models.PROTECT)
    plan = models.ForeignKey(TopupPlan, on_delete=models.PROTECT, null=True)

    amount = models.IntegerField(verbose_name="實際支付金額")
    points = models.IntegerField(verbose_name="實際獲得點數")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="完成支付時間")

    def __str__(self):
        return f"{self.order_id} ({self.status})"


# --- 訂單歷程紀錄 (狀態機日誌) ---
class TopupOrderLog(models.Model):
    order = models.ForeignKey(TopupOrder, on_delete=models.PROTECT, related_name='logs')
    from_status = models.CharField(max_length=15, verbose_name="原狀態")
    to_status = models.CharField(max_length=15, verbose_name="新狀態")
    operator = models.CharField(max_length=50, default="System", verbose_name="操作者")
    remark = models.TextField(blank=True, verbose_name="變動備註")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="紀錄時間")

    class Meta:
        ordering = ['-created_at']  # 最新的紀錄排在最前面

    def __str__(self):
        return f"{self.order.order_id}: {self.from_status} -> {self.to_status}"


# --- 球館權限管理 ---
class GymStaff(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_CLERK = 'clerk'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_CLERK, 'Clerk'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='gym_roles'
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.PROTECT,
        related_name='staff_roles'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CLERK)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'gym')
        verbose_name = "球館權限"
        verbose_name_plural = "球館權限"

    def __str__(self):
        return f"{self.user} @ {self.gym} ({self.role})"
