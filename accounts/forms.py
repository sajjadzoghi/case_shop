from django.contrib.auth import authenticate
from django import forms

from accounts.models import Address


class LoginForm(forms.Form):
    mobile = forms.CharField(min_length=11, max_length=11,
                             error_messages={'required': '.شماره موبایل وارد نشده',
                                             'min_length': '.شماره موبایل نامعتبر است',
                                             'max_length': '.شماره موبایل نامعتبر است'})
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': '.رمز عبور وارد نشده'})

    def clean(self):
        cleaned_data = self.data
        user = authenticate(mobile=cleaned_data['mobile'], password=cleaned_data['password'])
        if user is None:
            raise forms.ValidationError(".متاسفانه کاربری با مشخصات داده‌شده پیدا نشد")
        return cleaned_data


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['customer', ]
        error_messages = {
            'province': {'required': '.استان انتخاب نشده'},
            'city': {'required': '.شهر انتخاب نشده'},
            'exact_address': {'required': '.آدرس دقیق وارد نشده'},
            'apartment_number': {'required': '.پلاک وارد نشده'},
        }
