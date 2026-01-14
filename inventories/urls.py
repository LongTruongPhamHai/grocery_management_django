from django.urls import path
from . import views

app_name = "inventories"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("purchases/", views.purchase_receipt_list, name="purchase_list"),
    path("purchases/add/", views.purchase_receipt_create, name="purchase_create"),
]
