from django.contrib import admin
from .models import Invoice, InvoiceDetail


# =========================
# INLINE: INVOICE DETAIL
# =========================
class InvoiceDetailInline(admin.TabularInline):
    """
    Hiển thị chi tiết hóa đơn
    ngay trong trang Invoice
    """

    model = InvoiceDetail
    extra = 0  # không tạo sẵn dòng trống
    readonly_fields = ("subtotal",)

    # Autocomplete sản phẩm
    autocomplete_fields = ("product",)

    # BẮT BUỘC phải có khi dùng autocomplete_fields
    search_fields = ("product__name", "product__code")


# =========================
# ADMIN: INVOICE
# =========================
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin quản lý HÓA ĐƠN
    """

    # Cột hiển thị ngoài danh sách
    list_display = ("id", "created_at", "total_amount")

    # Lọc theo ngày bán
    list_filter = ("created_at",)

    # Tìm kiếm theo mã hóa đơn
    search_fields = ("id",)

    # Không cho sửa các field hệ thống
    readonly_fields = ("created_at", "total_amount")

    # Nhúng chi tiết hóa đơn
    inlines = [InvoiceDetailInline]

    # Hóa đơn mới nhất lên trước
    ordering = ("-created_at",)


# =========================
# ADMIN: INVOICE DETAIL
# =========================
@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    """
    Admin quản lý CHI TIẾT HÓA ĐƠN
    (xem riêng từng dòng sản phẩm)
    """

    list_display = (
        "invoice",
        "product",
        "quantity",
        "price_at_sale",
        "subtotal",
    )

    list_filter = ("invoice", "product")

    search_fields = (
        "invoice__id",
        "product__name",
        "product__code",
    )

    readonly_fields = ("subtotal",)

    # Autocomplete sản phẩm
    autocomplete_fields = ("product",)
