from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from accounts.models import Address

Customer = get_user_model()

EmailField.default_error_messages = {
    'invalid': '.آدرس ایمیل نامعتبر است'
}


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registration endpoint.
    """

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
                                     style={'input_type': 'password'},
                                     error_messages={'blank': '.رمز عبور وارد نشده', })
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'},
                                      error_messages={'blank': '.تکرار رمز عبور وارد نشده', })

    class Meta:
        model = Customer
        fields = ['mobile', 'first_name', 'last_name', 'email', 'password', 'password2']
        validators = [UniqueTogetherValidator(queryset=Customer.objects.all(), fields=['mobile', 'email'])]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(".رمز عبور وارد شده با تکرار آن برابر نیست")

        return attrs

    def create(self, validated_data):
        user = Customer.objects.create(
            mobile=validated_data['mobile'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangeMobileSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11, error_messages={'blank': '.شماره موبایل وارد نشده',
                                                                                 'min_length': '.شماره موبایل نامعتبر است',
                                                                                 'max_length': '.شماره موبایل نامعتبر است'},
                                   validators=[UniqueValidator(queryset=Customer.objects.all(),
                                                               message='.این شماره قبلاً توسط کاربری دیگر ثبت شده‌است')])

    class Meta:
        model = Customer
        fields = ['mobile']

    def update(self, instance, validated_data):
        instance.mobile = validated_data['mobile']
        instance.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                         error_messages={'blank': 'رمزعبور جدید وارد نشده.', })
    new_password2 = serializers.CharField(write_only=True, required=True,
                                          error_messages={'blank': 'تکرار رمزعبور جدید وارد نشده.', })
    old_password = serializers.CharField(write_only=True, required=True,
                                         error_messages={'blank': 'رمزعبور فعلی وارد نشده.', })

    class Meta:
        model = Customer
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("رمز عبور وارد شده با تکرار آن برابر نیست.")

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی صحیح نیست.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class ResetPasswordByMobileSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11, error_messages={'blank': '.شماره موبایل وارد نشده',
                                                                                 'min_length': '.شماره موبایل نامعتبر است',
                                                                                 'max_length': '.شماره موبایل نامعتبر است'}, )

    class Meta:
        model = Customer
        fields = ['mobile']


class ResetPasswordByEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(error_messages={'blank': '.ایمیل وارد نشده', }, )

    class Meta:
        model = Customer
        fields = ['email']


class ConfirmResetPasswordSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField()
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ['mobile', 'new_password', 'new_password2']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(".رمز عبور وارد شده با تکرار آن برابر نیست")

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.email')
    province = serializers.CharField(error_messages={'blank': 'استان وارد نشده.'})
    city = serializers.CharField(error_messages={'blank': 'شهر وارد نشده.', })
    exact_address = serializers.CharField(error_messages={'blank': 'آدرس وارد نشده.', })
    apartment_number = serializers.IntegerField(
        error_messages={'required': 'پلاک وارد نشده.', 'invalid': 'پلاک معتبر وارد نشده.'})
    unit = serializers.IntegerField(required=False)
    zip_code = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ['customer', 'province', 'city', 'exact_address', 'apartment_number', 'unit', 'zip_code', ]
