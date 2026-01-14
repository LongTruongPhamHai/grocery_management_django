from django import forms
from .models import Product, PurchaseReceipt


# ==================================
# FORM: PRODUCT
# ==================================
class ProductForm(forms.ModelForm):
    """
    Form dùng để thêm mới và chỉnh sửa sản phẩm
    Tự động ánh xạ các trường trong model Product
    """

    class Meta:
        # Model mà form này liên kết tới
        model = Product

        # Danh sách các field được phép hiển thị và nhập dữ liệu
        fields = ["code", "name", "unit", "price", "stock"]

        # Tùy chỉnh widget (HTML input) cho từng field
        # Mục đích: gắn class Bootstrap để giao diện đẹp hơn
        widgets = {
            # Ô nhập mã sản phẩm
            "code": forms.TextInput(attrs={"class": "form-control"}),
            # Ô nhập tên sản phẩm
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # Dropdown chọn đơn vị tính
            "unit": forms.Select(attrs={"class": "form-select"}),
            # Ô nhập giá bán
            # NumberInput giúp trình duyệt chỉ cho nhập số
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            # Ô nhập số lượng tồn kho
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
        }


# ==================================
# FORM: PURCHASE RECEIPT (PHIẾU NHẬP)
# ==================================
class PurchaseReceiptForm(forms.ModelForm):
    """
    Form dùng để tạo phiếu nhập hàng
    Khi lưu form, tồn kho sản phẩm sẽ được cập nhật
    (logic xử lý nằm trong model PurchaseReceipt)
    """

    class Meta:
        # Model mà form này liên kết tới
        model = PurchaseReceipt

        # Chỉ cho phép nhập các field cần thiết
        # total_price và datetime sẽ được tự động xử lý
        fields = ["product", "quantity", "unit_price"]

        # Tùy chỉnh giao diện input cho form
        widgets = {
            # Dropdown chọn sản phẩm
            "product": forms.Select(attrs={"class": "form-select"}),
            # Ô nhập số lượng nhập
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            # Ô nhập giá nhập cho mỗi đơn vị
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
        }
