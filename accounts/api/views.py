# This class returns the string needed to generate the key
import base64
import time
from datetime import datetime
# from kavenegar import *
import pyotp
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializer import CustomerSerializer

Customer = get_user_model()


class CustomerView(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateKey:
    @staticmethod
    def value(phone):
        return str(phone) + str(datetime.date(datetime.now()))


# get info to create a call for OTP
class GetInfo(APIView):
    # permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
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
            info = self.customer_data(request.data)
            serializer = CustomerSerializer(data=info)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'otp': ['.کد واردشده اشتباه است']}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def customer_data(info):
        return {item: info[item] for item in info if item != 'otp'}
