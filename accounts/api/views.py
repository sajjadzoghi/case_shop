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

from accounts.api.serializer import (RegistrationSerializer, ChangePasswordSerializer, ConfirmResetPasswordSerializer,
                                     ResetPasswordByMobileSerializer,
                                     ResetPasswordByEmailSerializer, AddressSerializer)
from accounts.models import Address
from shop.utils import send_reset_password_mail

Customer = get_user_model()


class GenerateKey:
    @staticmethod
    def value(item):
        return item + str(datetime.date(datetime.now()))


class CustomerData:
    @staticmethod
    def value(info):
        return {item: info[item] for item in info if item != 'otp'}


# class GetCustomer():
#     @staticmethod
#     def value(data):
#         try:
#             return Customer.objects.get(Q(mobile=data) | Q(email=data))
#         except Customer.DoesNotExist:
#             return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)


class CustomerView(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = RegistrationSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get info to create a call for OTP
class GetInfo(APIView):
    # permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(info['mobile']).encode())  # Key is generated
        totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created
        print(totp.now())  # only for cheating

        """
        using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        """
        # api = KavenegarAPI('33524B76642B4F4759646D66573648666B3575756D6E6A6D785A47662B4444524A5669664E564C71626D413D')
        # params = {'sender': '100047778', 'receptor': info['mobile'], 'message': f'کد تایید عضویت شما در کالاشاپ: {totp.now()}'}
        # response = api.sms_send(params)
        return Response(status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    # verifying the OTP

    def post(self, request):
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(request.data['mobile']).encode())  # Generating Key
        totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created

        if totp.verify(request.data['otp']):
            info = CustomerData.value(request.data)
            serializer = RegistrationSerializer(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordView(generics.UpdateAPIView):
    # An endpoint for changing password.

    queryset = Customer.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)


class RequestResetPasswordMobile(APIView):
    # An endpoint for requesting for resetting password by mobile number

    def post(self, request):
        try:
            customer = Customer.objects.get(mobile=request.data['mobile'])
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordByMobileSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(info['mobile']).encode())  # Key is generated
        totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created
        print(totp.now())  # only for cheating

        # using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
        return Response({'mobile': info['mobile']}, status=status.HTTP_200_OK)


class RequestResetPasswordEmail(APIView):
    # An endpoint for requesting for resetting password by Email

    def post(self, request):
        try:
            customer = Customer.objects.get(email=request.data['email'])
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordByEmailSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(info['email']).encode())  # Key is generated
        totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created
        print(totp.now())

        # using multi-threading send the OTP using Email services
        send_reset_password_mail(
            subject='درخواست بازیابی رمز عبور',
            message=f' {customer.first_name} عزیز، درخواست شما برای بازیابی رمز عبور دریافت شد. کد تایید شما جهت احراز هویت: {totp.now()}',
            recipient_list=[info['email']]
        )  # using multi-threading send the OTP using Email services
        return Response({'email': info['email']}, status=status.HTTP_200_OK)


class VerifyOTPResetPassword(APIView):
    # verifying the OTP

    def post(self, request):
        keygen = GenerateKey()
        key = base64.b32encode(keygen.value(request.data['info']).encode())  # Generating Key
        totp = pyotp.TOTP(key, interval=120)  # TOTP Model for OTP is created

        if totp.verify(request.data['otp']):
            customer = Customer.objects.get(Q(mobile=request.data['info']) | Q(email=request.data['info']))
            return Response({'mobile': customer.mobile,
                             'first_name': customer.first_name}, status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ConfirmResetPassword(APIView):
    # verifying the new password

    def post(self, request):
        customer = Customer.objects.get(mobile=request.data['mobile'])
        serializer = ConfirmResetPasswordSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'first_name': customer.first_name}, status=status.HTTP_200_OK)


class AddAddress(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)