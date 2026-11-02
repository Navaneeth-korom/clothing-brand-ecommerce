from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("T-Shirts", "T-Shirts"),
        ("Shirts", "Shirts"),
        ("Jeans", "Jeans"),
        ("Trousers", "Trousers"),
        ("Hoodies", "Hoodies"),
        ("Jackets", "Jackets"),
    ]

    SIZE_CHOICES = [
        ("XS", "Extra Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
        ("XXL", "Double Extra Large"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    sku = models.CharField(max_length=20, unique= True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email =  models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
