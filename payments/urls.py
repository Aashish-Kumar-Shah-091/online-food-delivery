from django.urls import path
from .views import payment_list, payment_detail, make_payment, checkout, esewa_success, esewa_failure

urlpatterns = [
    path('', payment_list, name='payment_list'),
    path('checkout/', checkout, name='checkout'),
    path('esewa/success/', esewa_success, name='esewa_success'),
    path('esewa/failure/', esewa_failure, name='esewa_failure'),
    path('<int:payment_id>/', payment_detail, name='payment_detail'),
    path('make/<int:order_id>/', make_payment, name='make_payment'),
]
