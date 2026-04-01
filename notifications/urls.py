from django.urls import path
from . views import notification_list, mark_as_read
urlpatterns = [
    path('notifications/',notification_list),
    path('notifications/',mark_as_read),
]