from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Payment
from orders.models import Order
# Create your views here.

@login_required
def payment_list(request):
    payments = Payment.objects.all()

    return render(
        request,
        'payments/payment_list.html',
        {'payments': payments}
    )


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id
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
        id=order_id
    )

    Payment.objects.create(
        order=order,
        payment_method='COD',
        payment_status='Completed'
    )

    return redirect('payment_list')