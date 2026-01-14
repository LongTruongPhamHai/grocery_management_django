from django.db import models, transaction
from django.db.models import F, Sum
from inventories.models import Product


# =========================
# MODEL: INVOICE (HÓA ĐƠN)
# =========================
class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày bán")

    total_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Tổng tiền"
    )

    def update_total_amount(self):
        """
        Tính lại tổng tiền hóa đơn
        = tổng subtotal của các InvoiceDetail
        """
        total = self.details.aggregate(total=Sum("subtotal"))["total"] or 0

        self.total_amount = total
        self.save(update_fields=["total_amount"])

    def __str__(self):
        return f"Hóa đơn #{self.pk} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"


# =====================================
# MODEL: INVOICE DETAIL (CHI TIẾT HÓA ĐƠN)
# =====================================
class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name="Hóa đơn",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Sản phẩm",
    )

    quantity = models.PositiveIntegerField(verbose_name="Số lượng")

    price_at_sale = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Giá bán lúc đó"
    )

    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, verbose_name="Thành tiền"
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # phân biệt tạo mới / cập nhật

        # Tính thành tiền
        self.subtotal = self.quantity * self.price_at_sale

        with transaction.atomic():
            super().save(*args, **kwargs)

            if is_new:
                # Kiểm tra tồn kho
                if self.product.stock < self.quantity:
                    raise ValueError("Số lượng tồn kho không đủ")

                # Trừ tồn kho
                Product.objects.filter(pk=self.product_id).update(
                    stock=F("stock") - self.quantity
                )

        # Cập nhật tổng tiền hóa đơn
        self.invoice.update_total_amount()

    def delete(self, *args, **kwargs):
        """
        Khi xóa chi tiết hóa đơn → hoàn lại tồn kho
        """
        with transaction.atomic():
            Product.objects.filter(pk=self.product_id).update(
                stock=F("stock") + self.quantity
            )
            super().delete(*args, **kwargs)

        self.invoice.update_total_amount()

    def __str__(self):
        return f"{self.invoice} - {self.product} x {self.quantity}"

    class Meta:
        verbose_name = "Chi tiết hóa đơn"
        verbose_name_plural = "Chi tiết hóa đơn"
