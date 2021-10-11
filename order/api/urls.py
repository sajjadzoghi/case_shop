from django.urls import path, include

from order.api.views import AddOrderItemsView, CheckCouponView

urlpatterns = [
    path('add-items/', AddOrderItemsView.as_view(), name='add_items'),
    path('check-coupon/', CheckCouponView.as_view(), name='check_coupon'),
]
