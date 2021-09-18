from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('all/', views.AllProductView.as_view(), name='all_product')
]
