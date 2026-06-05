
from django.contrib import admin
from django.urls import path
from . views import payment_list, payment_detail, make_payment

urlpatterns = [
    path('payments/',payment_list),
    path('payments/',payment_detail),
    path('payments/',make_payment),
]