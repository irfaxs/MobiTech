from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart
from products.models import Product


# ✅ ADD TO CART
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    # ✅ STOCK CHECK
    if created:
        if product.stock > 0:
            cart_item.quantity = 1
            cart_item.save()
    else:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    # ✅ STAY ON SAME PAGE
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


# ✅ VIEW CART
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ➕ INCREASE QUANTITY
@login_required
def increase_qty(request, pk):
    item = get_object_or_404(Cart, id=pk, user=request.user)

    # ✅ STOCK LIMIT CHECK
    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart_view')


# ➖ DECREASE QUANTITY (MIN = 1)
@login_required
def decrease_qty(request, pk):
    item = get_object_or_404(Cart, id=pk, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart_view')


# ❌ REMOVE ITEM
@login_required
def remove_item(request, pk):
    item = get_object_or_404(Cart, id=pk, user=request.user)
    item.delete()

    return redirect('cart_view')