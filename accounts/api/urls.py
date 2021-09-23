from django.urls import path, include

from accounts.api.views import GetInfo, CustomerView, VerifyOTP

urlpatterns = [
    path('register/', GetInfo.as_view(), name='get_info'),
    path('verify/', VerifyOTP.as_view(), name='verify_otp'),
    path('', CustomerView.as_view(), name='customer'),
]