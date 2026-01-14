from django import forms
from .models import Product, PurchaseReceipt


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["code", "name", "unit", "price", "stock"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PurchaseReceiptForm(forms.ModelForm):
    class Meta:
        model = PurchaseReceipt
        fields = ["product", "quantity", "unit_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
        }
