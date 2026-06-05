from django.db import models
from orders.models import Order

# Create your models here.

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment {self.id}"