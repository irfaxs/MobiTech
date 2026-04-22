from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:pk>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:pk>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:pk>/', views.remove_item, name='remove_item'),

]