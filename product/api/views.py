from rest_framework import generics, viewsets
from product.api.serializer import ProductSerializer
from product.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
