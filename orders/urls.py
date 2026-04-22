from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),

    # ❌ REMOVE OLD
    # path('history/', views.order_history, name='order_history'),

    # ✅ NEW MERGED PAGE
    path('my-orders/', views.all_orders, name='my_orders'),
]