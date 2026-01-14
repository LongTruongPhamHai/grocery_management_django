from django.db import models


# =========================
# MODEL: PRODUCT (SẢN PHẨM)
# =========================
class Product(models.Model):

    # Enum cho đơn vị tính
    # - Giá trị thứ nhất: lưu trong database
    # - Giá trị thứ hai: hiển thị ra giao diện (admin, form)
    class Unit(models.TextChoices):
        PIECE = "PCS", "Piece"
        PACK = "PKT", "Pack"
        CARTON = "CTN", "Carton"
        BOTTLE = "BTL", "Bottle"
        CAN = "CAN", "Can"
        KG = "KG", "Kilogram"

    # Mã sản phẩm / mã vạch
    # unique=True: đảm bảo mỗi sản phẩm có mã duy nhất
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã sản phẩm")

    # Tên sản phẩm
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")

    # Đơn vị tính của sản phẩm
    # Chỉ cho phép chọn các giá trị trong Unit
    unit = models.CharField(
        max_length=10, choices=Unit.choices, verbose_name="Đơn vị tính"
    )

    # Giá bán hiện tại của sản phẩm
    # Dùng DecimalField để đảm bảo chính xác tiền tệ
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Giá bán")

    # Số lượng tồn kho hiện tại
    # PositiveIntegerField: chỉ cho số >= 0
    stock = models.PositiveIntegerField(default=0, verbose_name="Tồn kho")

    # Chuỗi hiển thị khi in object (Admin, shell, ForeignKey)
    def __str__(self):
        return f"{self.code} - {self.name}"

    # Định nghĩa cách hiển thị model
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"


# ==============================
# MODEL: PURCHASE RECEIPT (PHIẾU NHẬP KHO)
# ==============================
class PurchaseReceipt(models.Model):

    # Sản phẩm được nhập kho
    # PROTECT: không cho xoá sản phẩm nếu đã từng có phiếu nhập
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_receipts",
        verbose_name="Sản phẩm",
    )

    # Số lượng sản phẩm nhập kho
    quantity = models.PositiveIntegerField(verbose_name="Số lượng nhập")

    # Giá nhập cho 1 đơn vị sản phẩm tại thời điểm nhập
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Giá nhập"
    )

    # Tổng tiền của phiếu nhập
    # Sẽ được tính tự động = unit_price * quantity
    total_price = models.DecimalField(
        max_digits=14, decimal_places=2, verbose_name="Tổng tiền"
    )

    # Thời gian tạo phiếu nhập
    # auto_now_add=True: tự động gán thời điểm tạo
    datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian nhập hàng"
    )

    # Ghi đè phương thức save()
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # chỉ cộng kho khi tạo mới

        # Tính tổng tiền
        self.total_price = self.unit_price * self.quantity

        super().save(*args, **kwargs)

        # Nếu là phiếu nhập mới → cộng tồn kho
        if is_new:
            self.product.stock += self.quantity
            self.product.save()

    # Chuỗi hiển thị cho phiếu nhập
    def __str__(self):
        return f"Nhập {self.product} - SL: {self.quantity}"

    class Meta:
        verbose_name = "Phiếu nhập"
        verbose_name_plural = "Phiếu nhập"
        ordering = ["-datetime"]  # phiếu nhập mới nhất hiển thị trước
