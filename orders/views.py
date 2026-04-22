from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
import razorpay
from .models import Order
from sell.models import SellRequest   # ✅ IMPORTANT

# ✅ CHECKOUT
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price() for item in cart_items)

    client = razorpay.Client(auth=("rzp_test_SXmYjsueDsovRq", "Z2Z4QcCIKk0NkzBS7wtgekR4"))

    payment = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'payment': payment
    })


# ✅ PAYMENT SUCCESS
@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')

    cart_items = Cart.objects.filter(user=request.user)

    orders = []
    total = 0

    for item in cart_items:
        item_total = item.total_price()

        order = Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item_total,
            payment_id=payment_id,
            address="Saved Address"
        )

        orders.append(order)
        total += item_total

        # 🔥 REDUCE STOCK
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    return render(request, 'orders/success.html', {
        'orders': orders,
        'total': total,
        'payment_id': payment_id
    })


# ✅ FINAL: MERGED ORDERS (BUY + SELL)
@login_required
def all_orders(request):

    buy_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # ⚠️ Using phone=username (your current logic)
    sell_orders = SellRequest.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/all_orders.html', {
        'buy_orders': buy_orders,
        'sell_orders': sell_orders
    })