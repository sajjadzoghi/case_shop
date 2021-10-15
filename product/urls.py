from django.urls import path
from product.views import AllProductView, ProductDetailView, CategoryProductsListView

app_name = 'product'
urlpatterns = [
    path('', AllProductView.as_view(), name='all_products'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<int:pk>', CategoryProductsListView.as_view(), name='categories_products'),
]
