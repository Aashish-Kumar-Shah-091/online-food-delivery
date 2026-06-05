
from django.contrib import admin
from django.urls import path
from . views import order_list, order_detail

urlpatterns = [
    path('orders/',order_list),
    path('orders/',order_detail),
]