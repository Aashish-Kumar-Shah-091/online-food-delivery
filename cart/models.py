from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.food_item.price * self.quantity