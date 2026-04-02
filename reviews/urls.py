from django.contrib import admin
from django.urls import path
from . views import review_list, add_review

urlpatterns = [
    path('reviews/',review_list),
    path('reviews/',add_review)
]