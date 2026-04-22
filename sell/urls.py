from django.urls import path
from . import views
from .views import (
    DeviceCreate,
    DeviceUpdate,
    DeviceDelete,
    BrandCreate,
    BrandUpdate,
    BrandDelete
)

urlpatterns = [

    # 🔥 BRAND CRUD (MUST BE FIRST)
    path('brand/add/', BrandCreate.as_view(), name='brand_create'),
    path('brand/<int:pk>/edit/', BrandUpdate.as_view(), name='brand_update'),
    path('brand/<int:pk>/delete/', BrandDelete.as_view(), name='brand_delete'),

    # 🔥 DEVICE CRUD
    path('add/', DeviceCreate.as_view(), name='device_create'),
    path('<int:pk>/edit/', DeviceUpdate.as_view(), name='device_update'),
    path('<int:pk>/delete/', DeviceDelete.as_view(), name='device_delete'),

    # 🔥 SUCCESS PAGE
    path('success/', views.sell_success, name='sell_success'),

    # 🔥 MAIN FLOW (KEEP BELOW CRUD)
    path('', views.select_brand, name='select_brand'),
    path('<str:brand_name>/', views.select_model, name='select_model'),

    # 🔥 DEVICE FLOW (MOST SPECIFIC LAST)
    path('<str:brand_name>/<str:device_name>/questions/', views.questions, name='questions'),
    path('<str:brand_name>/<str:device_name>/result/', views.result, name='result'),
    path('<str:brand_name>/<str:device_name>/booking/', views.booking, name='booking'),
    path('<str:brand_name>/<str:device_name>/', views.device_detail, name='device_detail'),
]