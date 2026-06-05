from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Restaurant(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)

    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name