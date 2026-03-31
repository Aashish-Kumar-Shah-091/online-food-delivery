from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from menu.models import FoodItem

# Create your views here.
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.all()

    total = sum(
        item.subtotal for item in cart_items
    )

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    }

    return render(
        request,
        'cart/cart.html',
        context
    )


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food_item=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect('cart')


@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == 'POST':
        quantity = int(
            request.POST.get('quantity', 1)
        )

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('cart')