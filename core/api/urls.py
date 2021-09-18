from django.urls import path, include

urlpatterns = [
    path('product/', include('product.api.urls')),
    path('order/', include('order.api.urls')),
    path('users/', include('accounts.api.urls')),
    path('auth/', include('rest_framework.urls')),
]