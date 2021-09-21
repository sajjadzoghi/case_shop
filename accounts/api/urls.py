from django.urls import path, include

from accounts.api.views import GetMobileNumberRegistered

urlpatterns = [
    path('register/', GetMobileNumberRegistered.as_view(), name='register')
]