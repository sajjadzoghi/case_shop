import base64
from datetime import datetime
# from kavenegar import *
import pyotp
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from accounts.api.permissions import IsOwnerOfAddress, IsOwnerOfPassword, IsOwnerOfMobile
from accounts.api.serializer import (RegistrationSerializer, ChangePasswordSerializer, ConfirmResetPasswordSerializer,
                                     ResetPasswordByMobileSerializer,
                                     ResetPasswordByEmailSerializer, AddressSerializer, ChangeMobileSerializer)
from accounts.models import Address
from shop.utils import send_reset_password_mail

Customer = get_user_model()

logger = logging.getLogger(__name__)


# a simple class for generating OTP based on 'mobile-number' or 'email'; so that it will be unique.
class GenerateKey:
    @staticmethod
    def value(item):
        item = item + str(datetime.date(datetime.now()))
        key = base64.b32encode(item.encode())  # Generating Key
        return pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created


# a class & staticmethod in order to remove 'otp' item from registration-info
class CustomerData:
    @staticmethod
    def value(info):
        return {item: info[item] for item in info if item != 'otp'}


# get user registration info, then create a call for OTP
class GetRegistrationInfoView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        totp = GenerateKey.value(info['mobile'])
        logger.debug(f"{info['first_name']} عزیز، کد تایید عضویت شما در کالاشاپ: {totp.now()}")  # only for cheating

        """
        using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        """
        # api = KavenegarAPI('33524B76642B4F4759646D66573648666B3575756D6E6A6D785A47662B4444524A5669664E564C71626D413D')
        # params = {'sender': '100047778', 'receptor': info['mobile'], 'message': f'کد تایید عضویت شما در کالاشاپ: {totp.now()}'}
        # response = api.sms_send(params)
        return Response(status=status.HTTP_200_OK)


# verifying the registration OTP
class VerifyRegistrationOTPView(APIView):

    def post(self, request):
        totp = GenerateKey.value(request.data['mobile'])
        if totp.verify(request.data['otp']):
            info = CustomerData.value(request.data)
            serializer = RegistrationSerializer(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


# An endpoint for changing mobile number.
class ChangeMobileView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        customer = request.user
        serializer = ChangeMobileSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        totp = GenerateKey.value(info['mobile'])
        logger.debug(f'کد تایید جهت ثبت شماره موبایل جدید: {totp.now()}')  # only for cheating

        """
        using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        """
        # api = KavenegarAPI('33524B76642B4F4759646D66573648666B3575756D6E6A6D785A47662B4444524A5669664E564C71626D413D')
        # params = {'sender': '100047778', 'receptor': info['mobile'], 'message': f'کد تایید عضویت شما در کالاشاپ: {totp.now()}'}
        # response = api.sms_send(params)
        return Response(status=status.HTTP_200_OK)


class VerifyOTPChangeMobile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        totp = GenerateKey.value(request.data['mobile'])
        if totp.verify(request.data['otp']):
            customer = request.user
            info = CustomerData.value(request.data)
            serializer = ChangeMobileSerializer(customer, data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


# An endpoint for changing password.
class ChangePasswordView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfPassword)


# An endpoint for requesting resetting password by mobile number
class RequestResetPasswordMobile(APIView):

    def post(self, request):
        try:
            customer = Customer.objects.get(mobile=request.data['mobile'])
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد.']}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordByMobileSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        totp = GenerateKey.value(info['mobile'])
        logger.debug(
            f"{customer.first_name} عزیز، کد تایید شما جهت بازیابی رمز عبور: {totp.now()}")  # only for cheating

        # using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        return Response({'mobile': info['mobile']}, status=status.HTTP_200_OK)


# An endpoint for requesting resetting password by Email
class RequestResetPasswordEmail(APIView):

    def post(self, request):
        try:
            customer = Customer.objects.get(email=request.data['email'])
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordByEmailSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        totp = GenerateKey.value(info['email'])
        logger.debug(
            f"{customer.first_name} عزیز، کد تایید شما جهت بازیابی رمز عبور: {totp.now()}")  # only for cheating

        # using multi-threading send the OTP using Email services
        send_reset_password_mail(
            subject='درخواست بازیابی رمز عبور',
            message=f' {customer.first_name} عزیز، درخواست شما برای بازیابی رمز عبور دریافت شد. کد تایید شما جهت احراز هویت:\n {totp.now()}',
            recipient_list=[info['email']]
        )  # using multi-threading send the OTP using Email services
        return Response({'email': info['email']}, status=status.HTTP_200_OK)


# verifying the OTP for resetting password
class VerifyOTPResetPassword(APIView):

    def post(self, request):
        totp = GenerateKey.value(request.data['info'])
        if totp.verify(request.data['otp']):
            customer = Customer.objects.get(Q(mobile=request.data['info']) | Q(email=request.data['info']))
            return Response({'mobile': customer.mobile,
                             'first_name': customer.first_name}, status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


# verifying the new password
class ConfirmResetPassword(APIView):

    def post(self, request):
        customer = Customer.objects.get(mobile=request.data['mobile'])
        serializer = ConfirmResetPasswordSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'first_name': customer.first_name}, status=status.HTTP_200_OK)


class AddAddressView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfAddress)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class EditRemoveAddressView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfAddress)

    def perform_update(self, serializer):
        serializer.save(customer=self.request.user)
