from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.views import ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='all_products')
]
