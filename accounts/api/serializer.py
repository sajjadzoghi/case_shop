from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

Customer = get_user_model()

EmailField.default_error_messages = {
    'invalid': '.آدرس ایمیل نامعتبر است'
}


class CustomerSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11, error_messages={'blank': '.شماره موبایل وارد نشده',
                                                                                 'min_length': '.شماره موبایل نامعتبر است',
                                                                                 'max_length': '.شماره موبایل نامعتبر است'},
                                   validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                               message='.این شماره قبلاً توسط کاربری دیگر ثبت شده‌است')])
    email = serializers.EmailField(error_messages={'blank': '.ایمیل وارد نشده', },
                                   validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                               message='.این ایمیل قبلاً توسط کاربری دیگر ثبت شده‌است')])
    first_name = serializers.CharField(error_messages={'blank': '.نام وارد نشده', })
    last_name = serializers.CharField(error_messages={'blank': '.نام‌خانوادگی وارد نشده', })
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})

    class Meta:
        model = Customer
        fields = ['mobile', 'first_name', 'last_name', 'email', 'password']
        validators = [UniqueTogetherValidator(queryset=Customer.objects.all(), fields=['mobile', 'email'])]
