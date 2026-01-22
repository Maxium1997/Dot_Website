from django.db import models
from django.conf import settings
from django.utils import timezone

from organization.models import Unit  # 導入 'Organization' 的 Unit 模型

from ckeditor.fields import RichTextField
import ckeditor

# >>>>>>>>>> Here is about Product >>>>>>>>>>


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = RichTextField(config_name='default')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 建議用 Decimal 存錢比較精準
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    is_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=5)
    stock = models.PositiveIntegerField(default=0)

    @property
    def price(self):
        """讓 variant.price 依然可用，實際上是回傳產品的價格"""
        return self.product.price

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"


# 新增一個模型來處理附屬品關聯
class ProductAccessory(models.Model):
    # 主產品 (例如：制服)
    main_product = models.ForeignKey(
        Product,
        related_name='accessory_relations',
        on_delete=models.CASCADE
    )
    # 附屬產品 (例如：加購的配件)
    accessory_item = models.ForeignKey(
        Product,
        related_name='is_accessory_to',
        on_delete=models.CASCADE
    )
    # 是否必選（選配或標配）
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.main_product.name} -> 附屬: {self.accessory_item.name}"

    class Meta:
        verbose_name = "附屬產品設定"
        unique_together = ('main_product', 'accessory_item')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', blank=True)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>> Here is about Credit Card >>>>>>>>>>


class MemberCredit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credits'  # 改為複數
    )
    fiscal_year = models.IntegerField(verbose_name="年度", help_text="例如：2026")
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00, verbose_name="初始額度")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00, verbose_name="剩餘額度")

    start_date = models.DateTimeField(verbose_name="開始使用日期")
    end_date = models.DateTimeField(verbose_name="到期日期")

    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 確保同一個使用者在同一個年度不會領到兩張卡
        unique_together = ('user', 'fiscal_year')
        ordering = ['-fiscal_year']
        verbose_name = "會員點數卡"
        verbose_name_plural = "會員點數卡"

    @property
    def is_currently_valid(self):
        """檢查此卡片在「現在」是否可用"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date and self.balance > 0

    def __str__(self):
        return f"{self.user.username} - {self.fiscal_year}年度點數卡"


class CreditTransaction(models.Model):
    class Status(models.TextChoices):
        PREPARING = 'PREPARING', '備貨中'
        COMPLETED = 'COMPLETED', '已完成'
        CANCELLED = 'CANCELLED', '已取消'

    credit_card = models.ForeignKey(
        'MemberCredit',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="消費金額")
    order_id = models.CharField(max_length=100, unique=True, verbose_name="關聯訂單編號", db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="交易時間")

    # 新增訂單狀態欄位
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PREPARING,
        verbose_name="訂單狀態",
        db_index=True
    )

    # 改為 TextField，因為原本的 CharField(255) 可能裝不下長長的清單
    description = models.TextField(blank=True, verbose_name="訂單明細內容")

    # 加入更新時間，追蹤狀態何時改變
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最後更新時間")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="取消時間")

    user_remark = models.TextField(blank=True, null=True, verbose_name="使用者備註")

    class Meta:
        verbose_name = "消費紀錄"
        verbose_name_plural = "消費紀錄"
        ordering = ['-timestamp']  # 預設依時間倒序排列

    def __str__(self):
        return f"{self.order_id} - {self.credit_card.user.username} ({self.get_status_display()})"


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# >>>>>>>>>> Here is about Whitelist Member >>>>>>>>>>


class WhitelistMember(models.Model):
    # 關聯至特定的服務單位
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='members',
        verbose_name="服務單位"
    )
    name = models.CharField(max_length=50, verbose_name="姓名")
    id_number = models.CharField(max_length=10, unique=True, verbose_name="身分證字號")
    birthday = models.DateField(verbose_name="生日")
    is_claimed = models.BooleanField(default=False, verbose_name="是否已領取卡片")

    # 2. 修改此處：將 'auth.User' 改為 settings.AUTH_USER_MODEL
    claimed_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='whitelist_info'
    )

    def __str__(self):
        # 這裡會用到 Unit 的 __str__，顯示包含上級單位的完整路徑
        return f"{self.unit} - {self.name}"

    class Meta:
        verbose_name = "白名單成員"
        verbose_name_plural = "白名單管理"


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
