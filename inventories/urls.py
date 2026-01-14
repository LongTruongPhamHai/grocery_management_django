from django.urls import path
from . import views


# Khai báo namespace cho app inventories
# Giúp phân biệt URL giữa các app khác nhau
# Ví dụ: {% url 'inventories:product_list' %}
app_name = "inventories"


# Danh sách các URL của app inventories
urlpatterns = [
    # ================= PRODUCT URLS =================
    # Danh sách sản phẩm
    # URL: /products/
    path("products/", views.product_list, name="product_list"),
    # Thêm mới sản phẩm
    # URL: /products/add/
    path("products/add/", views.product_create, name="product_create"),
    # Chỉnh sửa sản phẩm theo khóa chính (pk)
    # URL: /products/5/edit/
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    # Xóa sản phẩm theo khóa chính (pk)
    # URL: /products/5/delete/
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    # ================= PURCHASE URLS =================
    # Danh sách phiếu nhập hàng
    # URL: /purchases/
    path("purchases/", views.purchase_receipt_list, name="purchase_list"),
    # Tạo phiếu nhập hàng mới
    # URL: /purchases/add/
    path("purchases/add/", views.purchase_receipt_create, name="purchase_create"),
]
