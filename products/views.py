from django.shortcuts import render
from .models import Product
from django.views.generic import ListView
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
