from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, PurchaseReceipt
from .forms import ProductForm, PurchaseReceiptForm


# ---------- PRODUCT ----------
def product_list(request):
    query = request.GET.get("q", "")
    if query:
        products = Product.objects.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        ).order_by("name")
    else:
        products = Product.objects.all().order_by("name")
    return render(
        request, "inventories/product_list.html", {"products": products, "query": query}
    )


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã thêm sản phẩm!")
            return redirect("inventories:product_list")
    else:
        form = ProductForm()
    return render(
        request,
        "inventories/product_form.html",
        {"form": form, "title": "Thêm sản phẩm"},
    )


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật sản phẩm!")
            return redirect("inventories:product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "inventories/product_form.html",
        {"form": form, "title": "Sửa sản phẩm"},
    )


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Đã xóa sản phẩm!")
        return redirect("inventories:product_list")
    return render(
        request, "inventories/product_confirm_delete.html", {"product": product}
    )


# ---------- PURCHASE RECEIPT ----------
def purchase_receipt_list(request):
    receipts = (
        PurchaseReceipt.objects.select_related("product").all().order_by("-datetime")
    )
    return render(request, "inventories/purchase_list.html", {"receipts": receipts})


def purchase_receipt_create(request):
    if request.method == "POST":
        form = PurchaseReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã tạo phiếu nhập!")
            return redirect("inventories:purchase_list")
    else:
        form = PurchaseReceiptForm()
    return render(
        request,
        "inventories/purchase_form.html",
        {"form": form, "title": "Thêm phiếu nhập"},
    )
