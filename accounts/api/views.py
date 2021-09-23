# This class returns the string needed to generate the key
import base64
import time
from datetime import datetime

import pyotp
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializer import CustomerSerializer

Customer = get_user_model()


class CustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now()))


# get info to create a call for OTP
class GetInfo(APIView):
    # permission_classes = [NotAuthenticated]

    def post(self, request):
        print(request.data)
        print(request.POST)
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        try:
            customer = Customer.objects.get(
                mobile=info['mobile'])  # if Mobile already exists the take this else create New One
            if customer.exists():
                return Response({'detail': 'این شماره موبایل قبلا ثبت شده‌است.'}, )
        except Customer.DoesNotExist:
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(info['mobile']).encode())  # Key is generated
            totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created
            print(totp.now())
            # using multi-threading send the OTP using messaging services like kavenegar, Ghasedak,...
            return Response(info, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    # verifying the OTP
    def post(self, request):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(request.data['mobile']).encode())  # Generating Key
        totp = pyotp.TOTP(key, interval=90)  # TOTP Model for OTP is created

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            info = serializer.validated_data
            if totp.verify(info["otp"]):  # Verifying the OTP
                Customer.save()
                return Response({'approved': 'ثبت‌نام باموفقیت انجام شد'}, status=200)
            return Response({'detail': 'کد واردشده اشتباه بود. دوباره امتحان کنید.'}, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
