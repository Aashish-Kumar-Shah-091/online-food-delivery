
from django.contrib import admin
from django.urls import path
from . views import restaurant_list, restaurant_detail

urlpatterns = [
    path('orders/',restaurant_list),
    path('orders/',restaurant_detail),
]