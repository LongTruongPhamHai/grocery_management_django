from django.contrib import admin
from .models import Product, PurchaseReceipt


# =========================
# ADMIN: PURCHASE RECEIPT
# =========================
@admin.register(PurchaseReceipt)
class PurchaseReceiptAdmin(admin.ModelAdmin):
    """
    Admin quản lý lịch sử nhập kho
    """

    list_display = (
        "product",
        "quantity",
        "unit_price",
        "total_price",
        "datetime",
    )

    list_filter = ("datetime", "product")

    # BẮT BUỘC nếu dùng autocomplete_fields
    search_fields = ("product__name", "product__code")

    readonly_fields = ("total_price", "datetime")

    # Autocomplete sản phẩm khi nhập kho
    autocomplete_fields = ("product",)

    ordering = ("-datetime",)


# =========================
# ADMIN: PRODUCT
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin quản lý sản phẩm
    """

    list_display = ("code", "name", "unit", "price", "stock")

    search_fields = ("code", "name")

    list_filter = ("unit",)

    ordering = ("name",)
