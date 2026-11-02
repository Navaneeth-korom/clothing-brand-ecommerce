from django.contrib import admin
from .models import Product, Contact

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "size",
        "color",
        "price",
        "stock",
        "is_active",
    ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject","created_at"]
