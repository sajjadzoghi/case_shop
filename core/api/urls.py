from django.urls import path, include

urlpatterns = [
    path('', include('product.api.urls')),
    path('orders/', include('order.api.urls')),
    path('accounts/', include('accounts.api.urls')),
    path('auth/', include('rest_framework.urls')),
]