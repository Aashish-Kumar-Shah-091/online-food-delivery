from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Delivery
# Create your views here.

@login_required
def delivery_list(request):
    deliveries = Delivery.objects.all()

    context = {
        'deliveries': deliveries
    }

    return render(
        request,
        'delivery/delivery_list.html',
        context
    )


@login_required
def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(
        Delivery,
        id=delivery_id
    )

    context = {
        'delivery': delivery
    }

    return render(
        request,
        'delivery/delivery_detail.html',
        context
    )


@login_required
def update_delivery_status(request, delivery_id):
    delivery = get_object_or_404(
        Delivery,
        id=delivery_id
    )

    if request.method == 'POST':
        status = request.POST.get('status')

        delivery.status = status
        delivery.save()

    return redirect(
        'delivery_detail',
        delivery_id=delivery.id
    )