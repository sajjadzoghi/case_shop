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

# info = {'csrfmiddlewaretoken': ['n9wCqD1LykLTWRaMRostRj1iTAM0cdCk0NPyVMl84pA2wIvXVwAMusAljD2kkbBG'],
#         'reg-mobile': ['09154438187'], 'firstname': ['علی'], 'lastname': ['کریمی'], 'email': ['ha@yahoo.com'],
#         'reg-password': ['10169']}
#
# # for item in info:
# #         info[item] = info[item][0]
# print({item: info[item][0] for item in info})
