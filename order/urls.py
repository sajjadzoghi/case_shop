from django.urls import path
from order.views import (CreateOrder, ListOrder, DetailOrder, OrderResult, AddOrderAddress, AddOrderItem, )

app_name = 'order'
urlpatterns = [
    path('all/', ListOrder.as_view(), name='all_orders'),
    path('<int:pk>', DetailOrder.as_view(), name='order_detail'),
    path('create-order/', CreateOrder.as_view(), name='create_order'),
    path('add-item/', AddOrderItem.as_view(), name='add_item'),
    path('order-result/', OrderResult.as_view(), name='order_result'),
    path('add-address/', AddOrderAddress.as_view(), name='add_address'),
]
