from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.api.serializer import ProductSerializer, CategorySerializer
from product.models import Product, Category


class ProductResultsPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 3

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'num_pages': self.page.paginator.num_pages,
        })


# a view show list of all the products for homepage of the project.
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductResultsPagination


# a view show list of all categories.
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# a view show list of all the products for determined by the category.
class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductResultsPagination

    def get_queryset(self):
        category = self.kwargs['category_id']
        return Product.objects.filter(category__id=category)
