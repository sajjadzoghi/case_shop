from django.urls import path, include

from accounts.api.views import (GetRegistrationInfoView, VerifyRegistrationOTPView, ChangePasswordView,
                                VerifyOTPResetPassword, RequestResetPasswordEmail, RequestResetPasswordMobile,
                                ConfirmResetPassword, AddAddressView, EditRemoveAddressView, ChangeMobileView,
                                VerifyOTPChangeMobile)

urlpatterns = [
    path('register/', GetRegistrationInfoView.as_view(), name='send_info'),
    path('verify-otp/', VerifyRegistrationOTPView.as_view(), name='verify_otp'),
    path('change-mobile/', ChangeMobileView.as_view(), name='change_mobile'),
    path('change-mobile/verify-otp/', VerifyOTPChangeMobile.as_view(), name='verify_otp_change_mobile'),
    path('change-password/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
    path('add-address/', AddAddressView.as_view(), name='add_address'),
    path('edit-address/<int:pk>', EditRemoveAddressView.as_view(), name='edit_remove_address'),
    path('password-reset/by-email/', RequestResetPasswordEmail.as_view(), name='reset_password_email'),
    path('password-reset/by-mobile/', RequestResetPasswordMobile.as_view(), name='reset_password_mobile'),
    path('password-reset/verify-otp/', VerifyOTPResetPassword.as_view(), name='verify_otp_reset_password'),
    path('password-reset/confirm/', ConfirmResetPassword.as_view(), name='confirm_reset_password'),
]
