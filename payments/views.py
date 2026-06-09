import uuid
import hmac
import hashlib
import base64

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest

from .models import Payment
from orders.models import Order, OrderItem
from cart.models import Cart

ESEWA_TEST_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
ESEWA_VERIFY_URL = "https://rc-epay.esewa.com.np/api/epay/transaction/status/"
ESEWA_MERCHANT_CODE = "EPAYTEST"
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"


def generate_signature(message, secret_key):
    hmac_obj = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    cart_items = cart.items.all()
    subtotal = sum(item.subtotal for item in cart_items)
    delivery_fee = 50
    tax = 0
    total = subtotal + delivery_fee + tax

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'COD')
        address = request.POST.get('address', '')

        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.subtotal
            )

        cart.items.all().delete()

        if payment_method == 'ESEWA':
            transaction_uuid = f"FE-{order.id}-{uuid.uuid4().hex[:8]}"

            Payment.objects.create(
                order=order,
                payment_method='ONLINE',
                payment_status='Pending',
                transaction_id=transaction_uuid
            )

            total_str = str(int(total))
            subtotal_str = str(int(subtotal))
            delivery_fee_str = str(int(delivery_fee))
            tax_str = str(int(tax))

            signed_field_names = "total_amount,transaction_uuid,product_code"
            message = f"total_amount={total_str},transaction_uuid={transaction_uuid},product_code={ESEWA_MERCHANT_CODE}"
            signature = generate_signature(message, ESEWA_SECRET_KEY)

            context = {
                'esewa_url': ESEWA_TEST_URL,
                'amount': subtotal_str,
                'tax_amount': tax_str,
                'total_amount': total_str,
                'transaction_uuid': transaction_uuid,
                'product_code': ESEWA_MERCHANT_CODE,
                'product_delivery_charge': delivery_fee_str,
                'product_service_charge': '0',
                'success_url': request.build_absolute_uri('/payments/esewa/success/'),
                'failure_url': request.build_absolute_uri('/payments/esewa/failure/'),
                'signed_field_names': signed_field_names,
                'signature': signature,
            }
            return render(request, 'payments/esewa_form.html', context)

        else:
            Payment.objects.create(
                order=order,
                payment_method='COD',
                payment_status='Pending'
            )
            messages.success(request, f"Order #{order.id} placed! Pay on delivery.")
            return redirect('order_detail', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'total': total,
    }
    return render(request, 'payments/checkout.html', context)


@login_required
def esewa_success(request):
    import json
    import base64 as b64

    data = request.GET.get('data')
    if not data:
        messages.error(request, "Invalid payment response.")
        return redirect('order_list')

    try:
        decoded = json.loads(b64.b64decode(data).decode())
    except Exception:
        messages.error(request, "Could not decode payment response.")
        return redirect('order_list')

    transaction_uuid = decoded.get('transaction_uuid', '')
    status = decoded.get('status', '')
    total_amount = decoded.get('total_amount', '')

    try:
        payment = Payment.objects.get(transaction_id=transaction_uuid)
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('order_list')

    if status == 'COMPLETE':
        payment.payment_status = 'Completed'
        payment.save()

        payment.order.status = 'Accepted'
        payment.order.save()

        messages.success(request, f"Payment successful! Order #{payment.order.id} confirmed.")
        return redirect('order_detail', order_id=payment.order.id)
    else:
        payment.payment_status = 'Failed'
        payment.save()
        messages.error(request, "Payment was not completed.")
        return redirect('order_detail', order_id=payment.order.id)


@login_required
def esewa_failure(request):
    messages.error(request, "Payment failed or was cancelled. Please try again.")
    return redirect('order_list')


@login_required
def payment_list(request):
    payments = Payment.objects.filter(
        order__user=request.user
    ).order_by('-paid_at')

    return render(
        request,
        'payments/payment_list.html',
        {'payments': payments}
    )


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        order__user=request.user
    )

    return render(
        request,
        'payments/payment_detail.html',
        {'payment': payment}
    )


@login_required
def make_payment(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    Payment.objects.create(
        order=order,
        payment_method='COD',
        payment_status='Completed'
    )

    return redirect('payment_list')
