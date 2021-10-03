from django.urls import path, include

from accounts.api.views import (GetInfo, CustomerView, VerifyOTP, ChangePasswordView,
                                VerifyOTPResetPassword, RequestResetPasswordEmail, RequestResetPasswordMobile,
                                ConfirmResetPassword)

urlpatterns = [
    path('register/', GetInfo.as_view(), name='send_info'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('change-password/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/by-email/', RequestResetPasswordEmail.as_view(), name='reset_password_email'),
    path('password-reset/by-mobile/', RequestResetPasswordMobile.as_view(), name='reset_password_mobile'),
    path('password-reset/verify-otp/', VerifyOTPResetPassword.as_view(), name='verify_otp_reset_password'),
    path('password-reset/confirm/', ConfirmResetPassword.as_view(), name='confirm_reset_password'),
    path('', CustomerView.as_view(), name='customer'),
]
