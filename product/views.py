from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from product.models import Product


# Create your views here.


class AllProductView(TemplateView):
    template_name = 'product/all-products.html'
