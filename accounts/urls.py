from django.urls import path

from accounts.views import login_view, logout_view

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('add-address/', AddAddress.as_view(), name='add_address'),
]
