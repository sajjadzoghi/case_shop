from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.api.views import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
