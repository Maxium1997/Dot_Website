from django.contrib import admin
from django.utils import timezone
from .models import Gym, Court, MemberWallet, Booking, PointLog


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')
    search_fields = ('name',)


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('number', 'gym', 'price_per_hour', 'is_active')
    list_filter = ('gym', 'is_active')
    search_fields = ('number',)


@admin.register(MemberWallet)
class MemberWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym', 'points')
    list_filter = ('gym',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('points',)  # 建議錢包餘額設為唯讀，透過 Inline 或 Action 儲值較安全

    # 讓管理員可以直接在錢包頁面看到點數變動歷史
    class PointLogInline(admin.TabularInline):
        model = PointLog
        extra = 0
        readonly_fields = ('amount', 'reason', 'created_at')
        can_delete = False

    inlines = [PointLogInline]

    # 實作一個 Action，讓管理員能快速在列表頁幫選中的人儲值 (範例：固定加1000點)
    actions = ['add_1000_points']

    @admin.action(description="為選中錢包儲值 1000 點")
    def add_1000_points(self, request, queryset):
        for wallet in queryset:
            wallet.points += 1000
            wallet.save()
            PointLog.objects.create(
                wallet=wallet,
                amount=1000,
                reason="管理員後台手動儲值"
            )
        self.message_user(request, "已成功為所選錢包各儲值 1000 點。")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_date', 'start_time', 'court', 'user', 'status')
    list_filter = ('status', 'booking_date', 'court__gym')
    search_fields = ('user__username', 'court__number')
    date_hierarchy = 'booking_date'

    # 增加顏色標籤顯示狀態
    def get_status_display(self, obj):
        from django.utils.html import format_html
        colors = {
            'confirmed': 'green',
            'pending': 'orange',
            'cancelled': 'red',
        }
        return format_html(
            '<span style="color: {}; fw-bold">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )

    get_status_display.short_description = "預約狀態"


@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'reason', 'created_at')
    list_filter = ('wallet__gym', 'created_at')
    search_fields = ('wallet__user__username', 'reason')
