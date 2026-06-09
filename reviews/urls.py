from django.urls import path
from .views import review_list, add_review

urlpatterns = [
    path('', review_list, name='review_list'),
    path('add/<int:food_id>/', add_review, name='add_review'),
]
