
from django.contrib import admin
from django.urls import path
from . views import delivery_list, delivery_detail, update_delivery_status

urlpatterns = [
    path('delivery/',delivery_list),
    path('delivery/',delivery_detail),
    path('delivery/',update_delivery_status),
]