from django.urls import path
from . import views
from django.urls import path
from .views import ProductList, ProductDetail, LaptopList,AccessoryList,SearchResults,ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
     path('laptops/', LaptopList.as_view(), name='laptop_list'),
     path('accessories/', AccessoryList.as_view(), name='accessory_list'),
     path('search/', SearchResults.as_view(), name='search_results'),
     path('live-search/', views.live_search, name='live_search'),
     path('add/', ProductCreate.as_view(), name='product_create'),
     path('<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
     path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
]