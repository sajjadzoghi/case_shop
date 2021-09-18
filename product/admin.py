from django.contrib import admin
from product.models import Category, Product, Color, ProductMedia, ProductDiscount

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(ProductMedia)
admin.site.register(ProductDiscount)
