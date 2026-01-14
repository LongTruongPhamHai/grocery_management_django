from django.db import models, transaction
from django.db.models import F, Sum
from inventories.models import Product


# =========================
# MODEL: INVOICE
# =========================
class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sale Date")

    total_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Total Amount"
    )

    def update_total_amount(self):
        """
        Recalculates the total invoice amount
        Sum of all associated InvoiceDetail subtotals
        """
        total = self.details.aggregate(total=Sum("subtotal"))["total"] or 0

        self.total_amount = total
        self.save(update_fields=["total_amount"])

    def __str__(self):
        return f"Invoice #{self.pk} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"


# =====================================
# MODEL: INVOICE DETAIL
# =====================================
class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name="Invoice",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Product",
    )

    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    price_at_sale = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Unit Price (at Sale)"
    )

    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, verbose_name="Subtotal"
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check for creation vs update

        # Calculate subtotal
        self.subtotal = self.quantity * self.price_at_sale

        with transaction.atomic():
            super().save(*args, **kwargs)

            if is_new:
                # Inventory Check
                if self.product.stock < self.quantity:
                    raise ValueError("Insufficient stock levels")

                # Deduct from inventory
                Product.objects.filter(pk=self.product_id).update(
                    stock=F("stock") - self.quantity
                )

        # Refresh total invoice amount
        self.invoice.update_total_amount()

    def delete(self, *args, **kwargs):
        """
        Restores stock levels when an item is removed from an invoice
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
        verbose_name = "Invoice Detail"
        verbose_name_plural = "Invoice Details"
