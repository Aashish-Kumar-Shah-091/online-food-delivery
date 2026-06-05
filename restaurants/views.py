from django.shortcuts import render, get_object_or_404
from .models import Restaurant

# Create your views here.

def restaurant_list(request):
    restaurants = Restaurant.objects.all()

    return render(
        request,
        'restaurants/restaurant_list.html',
        {'restaurants': restaurants}
    )


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    return render(
        request,
        'restaurants/restaurant_detail.html',
        {'restaurant': restaurant}
    )