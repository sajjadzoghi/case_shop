# import base64
# from datetime import datetime
#
# import pyotp
#
# class generateKey:
#     @staticmethod
#     def returnValue(phone):
#         return str(phone) + str(datetime.date(datetime.now()))
#
# def a(phone):
#     keygen = generateKey()
#     key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
#     totp = pyotp.TOTP(key, interval=5)
#     print(totp.now())
#
# def b(phone):
#     keygen = generateKey()
#     key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
#     totp = pyotp.TOTP(key, interval=5)
#     print(totp.now())
#
#
# a(9154438187)
# b(9154438187)