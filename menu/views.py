from django.shortcuts import render, get_object_or_404
from .models import FoodItem, Category

# Create your views here.

def menu_list(request):
    foods = FoodItem.objects.all()

    context = {
        'foods': foods
    }

    return render(
        request,
        'menu/menu_list.html',
        context
    )


def food_detail(request, food_id):
    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    context = {
        'food': food
    }

    return render(
        request,
        'menu/food_detail.html',
        context
    )


def category_foods(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id
    )

    foods = FoodItem.objects.filter(
        category=category
    )

    context = {
        'category': category,
        'foods': foods
    }

    return render(
        request,
        'menu/category_foods.html',
        context
    )