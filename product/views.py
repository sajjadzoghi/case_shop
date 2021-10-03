from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView

from product.models import Product


# Create your views here.


class AllProductView(TemplateView):
    template_name = 'product/all-products.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product/product.html'
