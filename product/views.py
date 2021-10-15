from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView

from product.models import Product, Category


# Create your views here.

class AllProductView(TemplateView):
    template_name = 'product/all-products.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-detail.html'


class CategoryProductsListView(DetailView):
    model = Category
    template_name = 'product/category-products.html'
