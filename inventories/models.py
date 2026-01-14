from django.db import models


# =========================
# MODEL: PRODUCT (SẢN PHẨM)
# =========================
class Product(models.Model):

    # Enum đơn vị tính
    # - Giá trị thứ nhất: lưu trong database
    # - Giá trị thứ hai: hiển thị trên giao diện (admin, form)
    class Unit(models.TextChoices):
        PIECE = "PCS", "Piece"
        PACK = "PKT", "Pack"
        CARTON = "CTN", "Carton"
        BOTTLE = "BTL", "Bottle"
        CAN = "CAN", "Can"
        KG = "KG", "Kilogram"

    # Mã sản phẩm / Mã vạch
    # unique=True: đảm bảo mỗi sản phẩm có mã duy nhất
    code = models.CharField(max_length=50, unique=True, verbose_name="Product Code")

    # Tên sản phẩm
    name = models.CharField(max_length=200, verbose_name="Product Name")

    # Đơn vị tính
    # Giới hạn lựa chọn theo các giá trị đã định nghĩa trong class Unit
    unit = models.CharField(max_length=10, choices=Unit.choices, verbose_name="Unit")

    # Giá bán hiện tại
    # DecimalField được sử dụng để đảm bảo độ chính xác khi xử lý tiền tệ
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Selling Price"
    )

    # Số lượng tồn kho hiện tại
    # PositiveIntegerField: đảm bảo số lượng tồn không âm
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Level")

    # Chuỗi đại diện cho đối tượng (hiển thị trong admin, shell, log...)
    def __str__(self):
        return f"{self.code} - {self.name}"

    # Metadata cho model
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


# ==============================
# MODEL: PURCHASE RECEIPT (PHIẾU NHẬP HÀNG)
# ==============================
class PurchaseReceipt(models.Model):

    # Sản phẩm liên quan đến phiếu nhập
    # PROTECT: không cho phép xóa sản phẩm nếu đã có lịch sử nhập hàng
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_receipts",
        verbose_name="Product",
    )

    # Số lượng nhập
    quantity = models.PositiveIntegerField(verbose_name="Quantity Received")

    # Giá nhập cho mỗi đơn vị tại thời điểm nhập
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Unit Cost"
    )

    # Tổng giá trị của phiếu nhập
    # Tự động tính bằng: unit_price * quantity
    total_price = models.DecimalField(
        max_digits=14, decimal_places=2, verbose_name="Total Amount"
    )

    # Thời điểm tạo phiếu nhập
    # auto_now_add=True: tự động gán thời gian khi bản ghi được tạo
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Received Date")

    # Ghi đè phương thức save để xử lý logic nghiệp vụ
    def save(self, *args, **kwargs):
        # Kiểm tra xem đây có phải là bản ghi mới hay không
        is_new = self.pk is None

        # Tính tổng tiền của phiếu nhập
        self.total_price = self.unit_price * self.quantity

        # Lưu phiếu nhập vào database
        super().save(*args, **kwargs)

        # Nếu là phiếu nhập mới -> cập nhật số lượng tồn kho của sản phẩm
        if is_new:
            self.product.stock += self.quantity
            self.product.save()

    # Chuỗi đại diện cho đối tượng
    def __str__(self):
        return f"Purchase: {self.product} - Qty: {self.quantity}"

    # Metadata cho model
    class Meta:
        verbose_name = "Purchase Receipt"
        verbose_name_plural = "Purchase Receipts"
        ordering = ["-datetime"]  # Hiển thị các phiếu nhập mới nhất trước
