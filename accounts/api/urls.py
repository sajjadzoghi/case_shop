from django.urls import path, include

from accounts.api.views import (GetInfo, CustomerView, VerifyOTP, ChangePasswordView, ResetPassword,
                                VerifyOTPResetPassword)

urlpatterns = [
    path('register/', GetInfo.as_view(), name='send_info'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', ResetPassword.as_view(), name='password_reset'),
    path('password-reset/verify-otp/', VerifyOTPResetPassword.as_view(), name='password_reset_verify_otp'),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('', CustomerView.as_view(), name='customer'),
]
