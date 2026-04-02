from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Review
from menu.models import FoodItem
# Create your views here.

def review_list(request):
    reviews = Review.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'reviews/review_list.html',
        {'reviews': reviews}
    )


@login_required
def add_review(request, food_id):
    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            food_item=food,
            rating=rating,
            comment=comment
        )

        return redirect('review_list')

    return render(
        request,
        'reviews/add_review.html',
        {'food': food}
    )