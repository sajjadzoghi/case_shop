from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import EmailField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

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

    class Meta:
        model = Customer
        fields = ['mobile', 'first_name', 'last_name', 'email', 'password']
        validators = [UniqueTogetherValidator(queryset=Customer.objects.all(), fields=['mobile', 'email'])]

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": ".رمز عبور وارد شده با تکرار آن برابر نیست"})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": ".رمز عبور فعلی صحیح نیست"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class UpdateCustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if Customer.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": ""})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()

        return instance


class ResetPasswordByMobile(serializers.ModelSerializer):
    mobile = serializers.CharField(min_length=11, max_length=11, error_messages={'blank': '.شماره موبایل وارد نشده',
                                                                                 'min_length': '.شماره موبایل نامعتبر است',
                                                                                 'max_length': '.شماره موبایل نامعتبر است'}, )

    class Meta:
        model = Customer
        fields = ['mobile']


class ResetPassword(serializers.ModelSerializer):
    email = serializers.EmailField(error_messages={'blank': '.ایمیل وارد نشده', }, )
    mobile = serializers.CharField(min_length=11, max_length=11, error_messages={'blank': '.شماره موبایل وارد نشده',
                                                                                 'min_length': '.شماره موبایل نامعتبر است',
                                                                                 'max_length': '.شماره موبایل نامعتبر است'}, )

    class Meta:
        model = Customer
        fields = ['email']


class ConfirmResetPassword(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Customer
        fields = ['new_password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
