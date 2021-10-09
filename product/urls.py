from django.urls import path
from product.views import AllProductView, ProductView

app_name = 'product'
urlpatterns = [
    path('', AllProductView.as_view(), name='all_products'),
    path('<int:pk>', ProductView.as_view(), name='product_detail'),
]
