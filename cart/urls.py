
from django.contrib import admin
from django.urls import path
from . views import cart_view, add_to_cart, remove_from_cart, update_quantity

urlpatterns = [
    path('cart/',cart_view),
    path('cart/',add_to_cart),
    path('cart/',remove_from_cart),
    path('cart/',update_quantity),
]