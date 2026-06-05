from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

# Create your models here.
class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=50,
        default='Assigned'
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery #{self.id}"