from django.contrib import admin
from product.models import Category, Product, Color, ProductImage, ProductDiscount

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(ProductImage)
admin.site.register(ProductDiscount)
