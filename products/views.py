from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.filter(is_active= True)
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        if search:
            queryset = queryset.filter(name__icontains= search)
        if category:
            queryset = queryset.filter(category= category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.objects.filter(is_active= True).values_list("category", flat=True).distinct()
        return context
    

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product-details.html"
    context_object_name = "product"

