from django.contrib import admin
from .models import Product

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
