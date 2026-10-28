from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product



def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("product_detail", pk=product_id)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect("product_detail", pk=product_id)

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("product_detail", pk=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product
    ).first()

    existing_quantity = cart_item.quantity if cart_item else 0
    new_quantity = existing_quantity + quantity

    if new_quantity > product.stock:
        messages.error(request, "Unavailable quantity.")
        return redirect("product_detail", pk=product_id)

    if cart_item:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    messages.success(request, f"{product.name} added to cart.")
    return redirect("cart")


def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_amount": total_amount,
    }
    return render(request, "orders/cart.html", context)