from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import WhitelistMember
from .models import Category, Product, ProductVariant, ProductAccessory, ProductImage


# 讓規格可以在產品頁面直接編輯
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# 讓多圖上傳可以在產品頁面直接編輯
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# 讓附屬品可以在產品頁面直接勾選
class ProductAccessoryInline(admin.TabularInline):
    model = ProductAccessory
    fk_name = 'main_product'    # 必須指定外鍵名稱，因為有兩個對外鍵指向同一個 model
    extra = 1
    verbose_name = "附屬加購品"
    verbose_name_plural = "附屬加購品設定"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_public']
    prepopulated_fields = {'slug': ('name',)}   # 自動根據名稱生成 slug


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'is_display', 'created_at']
    list_filter = ['category', 'is_active', 'is_display']
    search_fields = ['name', 'description']
    inlines = [ProductVariantInline, ProductImageInline, ProductAccessoryInline]


# 定義哪些欄位可以匯入
class WhitelistMemberResource(resources.ModelResource):
    class Meta:
        model = WhitelistMember
        fields = ('id', 'name', 'id_number', 'birthday') # 與 Excel 欄位對應
        import_id_fields = ('id_number',)   # 以身分證作為唯一判斷基準


@admin.register(WhitelistMember)
class WhitelistMemberAdmin(ImportExportModelAdmin):
    resource_class = WhitelistMemberResource
    list_display = ['name', 'id_number', 'birthday', 'is_claimed', 'claimed_by']
    search_fields = ['name', 'id_number']
    list_filter = ['is_claimed']


from django.contrib import admin
from .models import MemberCredit, CreditTransaction


# 讓消費紀錄以列表形式出現在點數卡下方
class CreditTransactionInline(admin.TabularInline):
    model = CreditTransaction
    extra = 0  # 預設不額外顯示空白列
    readonly_fields = ('timestamp', 'amount', 'order_id', 'description')  # 通常紀錄不應被隨意修改
    can_delete = False  # 防止誤刪消費紀錄


@admin.register(MemberCredit)
class MemberCreditAdmin(admin.ModelAdmin):
    # 列表頁顯示的資訊
    list_display = (
        'user',
        'fiscal_year',
        'initial_balance',
        'balance',
        'start_date',
        'end_date',
        'is_active'
    )

    # 右側篩選器
    list_filter = ('fiscal_year', 'is_active', 'start_date')

    # 搜尋功能（可搜尋使用者名稱）
    search_fields = ('user__username', 'user__email')

    # 內嵌消費紀錄
    inlines = [CreditTransactionInline]

    # 欄位分組佈局
    fieldsets = (
        ('基本資訊', {
            'fields': ('user', 'fiscal_year', 'is_active')
        }),
        ('額度管理', {
            'fields': ('initial_balance', 'balance')
        }),
        ('使用期限', {
            'fields': ('start_date', 'end_date')
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:  # 如果是修改現有資料
            old_obj = MemberCredit.objects.get(pk=obj.pk)
            if old_obj.balance != obj.balance:
                diff = obj.balance - old_obj.balance
                CreditTransaction.objects.create(
                    credit_card=obj,
                    amount=diff,
                    order_id="ADMIN_ADJUST",
                    description=f"管理員 {request.user.username} 手動調整額度 (差異: {diff})"
                )
        super().save_model(request, obj, form, change)


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'amount', 'order_id', 'timestamp', 'status')
    list_filter = ('timestamp',)
    search_fields = ('order_id', 'credit_card__user__username')
    readonly_fields = ('credit_card', 'amount', 'order_id', 'timestamp', 'status')

    # 輔助方法：在清單顯示使用者名稱
    def get_user(self, obj):
        return obj.credit_card.user.username

    get_user.short_description = '使用者'
