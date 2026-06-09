from django.urls import path
from .views import restaurant_list, restaurant_detail

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),
    path('<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
]
