from django import forms
from .models import InvoiceDetail, Invoice
from inventories.models import Product


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = []  # tạo hóa đơn mới chỉ cần auto tạo ngày, total_amount auto tính


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ["product", "quantity", "price_at_sale"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price_at_sale": forms.NumberInput(attrs={"class": "form-control"}),
        }
