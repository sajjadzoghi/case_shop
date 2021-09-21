# class ValidatePhoneSendOTP(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         name = request.data.get('name', False)
#         phone_number = request.data.get('phone')
#         if phone_number:
#             phone = str(phone_number)
#             user = User.objects.filter(phone__iexact=phone)
#
#             if user.exists():
#                 return Response({
#                     'status': False,
#                     'detail': 'Phone number already exists.'
#                 })
#             else:
#                 key = send_otp(phone)
#
#                 if key:
#                     old = Customer.objects.filter(phone__iexact=phone)
#                     if old.exists():
#                         old = old.first()
#                         count = old.count
#                         # if count > 20:
#                         #     return Response({
#                         #         'status': False,
#                         #         'detail' : 'Sending otp error. Limit Exceeded. Please contact customer support.'
#                         #         })
#                         old.count = count + 1
#                         old.save()
#                         print('Count Increase', count)
#                         return Response({
#                             'status': True,
#                             'detail': 'OTP sent successfully.'
#                         })
#                     else:
#                         PhoneOTP.objects.create(
#                             # name = name,
#                             phone=phone,
#                             otp=key,
#                         )
#                         link = f'API-urls'
#                         requests.get(link)
#                         return Response({
#                             'status': True,
#                             'detail': 'OTP sent successfully.'
#                         })
#                 else:
#                     return Response({
#                         'status': False,
#                         'detail': 'Sending OTP error.'
#                     })
#         else:
#             return Response({
#                 'status': False,
#                 'detail': 'Phone number is not given in post request.'
#             })
#
#
# def send_otp(phone):
#     if phone:
#         key = random.randint(999, 9999)
#         print(key)
#         return key
#     else:
#         return False
#
#
# class ValidateOTP(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         phone = request.data.get('phone', False)
#         otp_sent = request.data.get('otp', False)
#
#         if phone and otp_sent:
#             old = Phone.objects.filter(phone__iexact=phone)
#             if old.exists():
#                 old = old.first()
#                 otp = old.otp
#                 if str(otp_sent) == str(otp):
#                     old.validated = True
#                     old.save()
#                     return Response({
#                         'status': True,
#                         'detail': 'OTP mactched. Please proceed for registration.'
#                     })
#
#                 else:
#                     return Response({
#                         'status': False,
#                         'detail': 'OTP incorrect.'
#                     })
#             else:
#                 return Response({
#                     'status': False,
#                     'detail': 'First proceed via sending otp request.'
#                 })
#         else:
#             return Response({
#                 'status': False,
#                 'detail': 'Please provide both phone and otp for validations'
#             })
