from django.urls import path, include

from order.api.views import AddOrderItemsView

urlpatterns = [
    path('add-items/', AddOrderItemsView.as_view(), name='add_items'),
]
