from django.shortcuts import render
from django.views import generic
from product.models import Product


# Create your views here.


class AllProductView(generic.ListView):
    template_name = 'product/all-product.html'
    context_object_name = 'all_products'

    def get_queryset(self):
        return Product.objects.all()
