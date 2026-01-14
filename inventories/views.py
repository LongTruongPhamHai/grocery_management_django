from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, PurchaseReceipt
from .forms import ProductForm, PurchaseReceiptForm


# ==================================
# CÁC VIEW LIÊN QUAN ĐẾN PRODUCT
# ==================================


def product_list(request):
    """
    Hiển thị danh sách sản phẩm
    - Hỗ trợ tìm kiếm theo mã sản phẩm hoặc tên sản phẩm
    - Nếu không nhập từ khóa thì hiển thị toàn bộ danh sách
    """

    # Lấy từ khóa tìm kiếm từ query string (?q=...)
    query = request.GET.get("q", "")

    if query:
        # Nếu có từ khóa -> lọc theo mã hoặc tên sản phẩm (không phân biệt hoa thường)
        products = Product.objects.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        ).order_by("name")
    else:
        # Nếu không có từ khóa -> lấy toàn bộ sản phẩm
        products = Product.objects.all().order_by("name")

    # Render template và truyền danh sách sản phẩm + từ khóa tìm kiếm
    return render(
        request,
        "inventories/product_list.html",
        {
            "products": products,
            "query": query,
        },
    )


def product_create(request):
    """
    Thêm mới sản phẩm
    - GET: hiển thị form nhập sản phẩm
    - POST: xử lý dữ liệu và lưu vào database
    """

    if request.method == "POST":
        # Nhận dữ liệu gửi lên từ form
        form = ProductForm(request.POST)

        # Kiểm tra dữ liệu hợp lệ
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("inventories:product_list")
    else:
        # Truy cập bằng GET -> hiển thị form trống
        form = ProductForm()

    return render(
        request,
        "inventories/product_form.html",
        {
            "form": form,
            "title": "Add New Product",
        },
    )


def product_update(request, pk):
    """
    Cập nhật thông tin sản phẩm
    - pk: khóa chính của sản phẩm
    - Nếu không tìm thấy sản phẩm -> trả về lỗi 404
    """

    # Lấy sản phẩm theo khóa chính
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        # Gắn instance=product để cập nhật bản ghi hiện tại
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("inventories:product_list")
    else:
        # Hiển thị form với dữ liệu sản phẩm hiện tại
        form = ProductForm(instance=product)

    return render(
        request,
        "inventories/product_form.html",
        {
            "form": form,
            "title": "Edit Product",
        },
    )


def product_delete(request, pk):
    """
    Xóa sản phẩm
    - GET: hiển thị trang xác nhận xóa
    - POST: thực hiện xóa sản phẩm
    """

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("inventories:product_list")

    return render(
        request,
        "inventories/product_confirm_delete.html",
        {
            "product": product,
        },
    )


# ==================================
# CÁC VIEW LIÊN QUAN ĐẾN PHIẾU NHẬP
# ==================================


def purchase_receipt_list(request):
    """
    Hiển thị danh sách phiếu nhập hàng
    - Sử dụng select_related để tối ưu truy vấn product
    - Sắp xếp theo thời gian tạo (mới nhất trước)
    """

    receipts = (
        PurchaseReceipt.objects.select_related("product").all().order_by("-datetime")
    )

    return render(
        request,
        "inventories/purchase_list.html",
        {
            "receipts": receipts,
        },
    )


def purchase_receipt_create(request):
    """
    Tạo phiếu nhập hàng mới
    - Khi lưu phiếu nhập, tồn kho sản phẩm sẽ tự động được cập nhật
      (logic đã xử lý trong phương thức save() của model)
    """

    if request.method == "POST":
        form = PurchaseReceiptForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Purchase receipt created successfully!")
            return redirect("inventories:purchase_list")
    else:
        form = PurchaseReceiptForm()

    return render(
        request,
        "inventories/purchase_form.html",
        {
            "form": form,
            "title": "Create Purchase Receipt",
        },
    )
