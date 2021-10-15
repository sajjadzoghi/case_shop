from django.urls import path
from order.views import (CreateOrder, AddOrderItem, order_result, )

app_name = 'order'
urlpatterns = [
    path('create-order/', CreateOrder.as_view(), name='create_order'),
    path('add-item/', AddOrderItem.as_view(), name='add_item'),
    path('order-result/', order_result, name='order_result'),
]
