from django.urls import path, include

from accounts.api.views import GetInfo, CustomerView, VerifyOTP

urlpatterns = [
    path('register/', GetInfo.as_view(), name='send_info'),
    path('verify/', VerifyOTP.as_view(), name='verify_otp'),
    path('', CustomerView.as_view(), name='customer'),
]