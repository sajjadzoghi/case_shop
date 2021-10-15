from django.urls import path

from accounts.views import login_view, logout_view, profile_view, OrdersHistoryView

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('orders-history/', OrdersHistoryView.as_view(), name='orders_history'),
]
