from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.views import ProductListView, CategoryListView, ProductListByCategory

urlpatterns = [
    path('products/', ProductListView.as_view(), name='all_products'),
    path('categories/', CategoryListView.as_view(), name='all_categories'),
    path('category/<int:category_id>', ProductListByCategory.as_view(), name='category_products'),
]
