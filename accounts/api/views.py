# This class returns the string needed to generate the key
import base64
from datetime import datetime, time

import pyotp
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
Customer = get_user_model()


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now()))


class GetMobileNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def post(request, phone):
        try:
            customer = Customer.objects.get(mobile=phone)  # if Mobile already exists the take this else create New One
            if customer.exists():
                return Response({'detail': 'این شماره موبایل قبلا ثبت شده‌است.'})
        except ObjectDoesNotExist:
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
            OTP = pyotp.TOTP(key)  # TOTP Model for OTP is created
            print(OTP.now())
            # using multi-threading send the OTP using messaging services like kavenegar, Ghasedak
            return Response({"OTP": OTP.now()}, status=200)  # Just for showing

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            time.sleep(5)
            Customer.objects.create(mobile=phone)
            return Response({'detail': 'ثبت‌نام باموفقیت انجام شد'}, status=200)
        return Response("OTP اشتباه است.", status=400)
