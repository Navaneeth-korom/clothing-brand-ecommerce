from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique= True)
    phone = models.CharField(max_length=10, blank= True)

    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    address_line = models.TextField(max_length= 255)
    city = models.CharField(max_length= 100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.full_name} - {self.city}"

    
