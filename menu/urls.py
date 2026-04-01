from django.urls import path
from . views import menu_list, food_detail, category_foods

urlpatterns = [
    path('delivery/',menu_list),
    path('delivery/',food_detail),
    path('delivery/',category_foods),
]