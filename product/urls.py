from django.urls import path
from product.views import AllProductView

app_name = 'product'
urlpatterns = [
    path('', AllProductView.as_view(), name='all_product')
]
