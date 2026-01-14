"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # Import module admin của Django để quản lý admin site
from django.urls import (
    path,
    include,
)  # Import path (định nghĩa URL) và include (gộp URL của các app)
from django.views.generic import (
    TemplateView,
)  # Import generic view TemplateView để render template tĩnh

urlpatterns = [
    # URL quản trị admin của Django
    path("admin/", admin.site.urls),
    # Trang chủ của website, render template home.html
    # Đây là cách dùng TemplateView cho trang tĩnh không cần viết view function
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Include các URL của app inventories (sản phẩm, phiếu nhập)
    # Tất cả URL trong inventories.urls sẽ được tiền tố "inventories/"
    path("inventories/", include("inventories.urls")),
    # Include các URL của app sales (hóa đơn, chi tiết hóa đơn)
    # Tất cả URL trong sales.urls sẽ được tiền tố "sales/"
    path("sales/", include("sales.urls")),
]
