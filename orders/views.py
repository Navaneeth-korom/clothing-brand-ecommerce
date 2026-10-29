from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from accounts.models import Address


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("product_details", pk=product_id)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.", extra_tags="product")
        return redirect("product_details", pk=product_id)

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.", extra_tags="product")
        return redirect("product_details", pk=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item = CartItem.objects.filter(
        cart=cart,
        product=product
    ).first()

    existing_quantity = cart_item.quantity if cart_item else 0
    new_quantity = existing_quantity + quantity

    if new_quantity > product.stock:
        messages.error(request, "Unavailable quantity.", extra_tags="product")
        return redirect("product_details", pk=product_id)

    if cart_item:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    messages.success(request, f"{product.name} added to cart.", extra_tags="cart")
    return redirect("cart")

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related("product")
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_amount": total_amount,
    }
    return render(request, "orders/cart.html", context)


@login_required
def update_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")

    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.", extra_tags="cart")
        return redirect("cart")

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.", extra_tags="cart")
    elif quantity > cart_item.product.stock:
        messages.error(
            request,
            "Requested quantity exceeds available stock.",
            extra_tags="cart",
        )
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart quantity updated.", extra_tags="cart")
    return redirect("cart")


@login_required
def remove_from_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart")

    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(
        request,
        f"{product_name} removed from your cart.",
        extra_tags="cart",
    )
    return redirect("cart")

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    addresses = Address.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    selected_address = None
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        if address_id and address_id != "new":
            selected_address = get_object_or_404(Address, id= address_id, user= request.user)
        else:
            full_name = request.POST.get("full_name").strip()
            address_line = request.POST.get("address_line").strip()
            city = request.POST.get("city").strip()
            state = request.POST.get("state").strip()
            postal_code = request.POST.get("postal_code").strip()
            if (not full_name or 
                not address_line or 
                not city or 
                not state or 
                not postal_code):
                messages.error(request, "Please fill in all address fields.",extra_tags="checkout")
                redirect("checkout")
            else:
                selected_address = Address.objects.create(
                    user=request.user,
                    full_name=full_name,
                    address_line=address_line,
                    city=city,
                    state=state,
                    postal_code=postal_code
                )
        
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "addresses": addresses,
        "total": total,
        "selected_address": selected_address,
    }
    return render(request, "orders/checkout.html", context)

@login_required
def place_order(request):
    if request.method == "POST":
        address_id = request.POST.get("confirmed_address_id")
        selected_address = get_object_or_404(Address, id=address_id, user=request.user)
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart= cart)
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, "Unavailable Quantity", extra_tags="place_order")
                return redirect("cart")
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            address=selected_address,
            total_amount= total_amount 
        )

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock = item.product.stock - item.quantity
            item.product.save()
        cart_items.delete()
        
        return render(request, "orders/confirmed-order.html",{"order": order})


        



