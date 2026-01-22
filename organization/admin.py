from django.contrib import admin

# from .models import Administration, Branch, CoastPatrolCorps, InternalUnit, InspectionOffice, PatrolStation, Brigade
# Register your models here.


from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.html import format_html

from django.contrib import admin
from django.utils.html import format_html
from .models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    # 1. 列表頁顯示的欄位
    list_display = ('id', 'name', 'en_name', 'serial_number', 'get_superior_display', 'director', 'landline_phone')

    # 2. 搜尋欄位（支援搜尋單位名稱、英文名、海巡 6 碼、長官姓名）
    search_fields = ('name', 'en_name', 'serial_number', 'director')

    # 3. 過濾器（右側選單，方便快速篩選）
    list_filter = ('superior_content_type',)

    # 4. 表單分組設定，讓輸入介面更有條理
    fieldsets = (
        ('基本資訊', {
            'fields': (('name', 'en_name'), 'serial_number', 'address')
        }),
        ('聯絡與通訊', {
            'fields': ('landline_phone', 'email')
        }),
        ('組織階層 (上級單位)', {
            'description': '請先選擇上級單位的類型（模型），再填入該單位的 ID。',
            'fields': ('superior_content_type', 'superior_object_id')
        }),
        ('主管人員', {
            'fields': ('director', 'deputy_director1', 'deputy_director2', 'deputy_director3')
        }),
    )

    # 5. 自定義方法：在列表中美化上級單位的顯示
    def get_superior_display(self, obj):
        if obj.superior:
            return format_html("<b>{}</b>", str(obj.superior))
        return "— (最高層級)"

    get_superior_display.short_description = '上級單位'

    # 6. 優化查詢效能 (避免 N+1 問題)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 預先載入 ContentType，減少資料庫查詢次數
        return qs.select_related('superior_content_type')

    # 7. (選配) 在修改頁面顯示下屬清單（唯讀）
    readonly_fields = ('show_subordinates_list',)

    def show_subordinates_list(self, obj):
        if not obj.id:
            return "儲存後顯示"
        subs = obj.get_all_subordinates()
        if not subs:
            return "無下屬單位"
        return format_html("<br>".join([sub.name for sub in subs]))

    show_subordinates_list.short_description = "所有下屬單位預覽"
