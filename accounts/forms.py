from django.contrib.auth import authenticate
from django import forms


class LoginForm(forms.Form):
    mobile = forms.CharField(label=':شماره موبایل', min_length=11, max_length=11, error_messages={'required': '.شماره موبایل وارد نشده',
                                                                           'min_length': '.شماره موبایل نامعتبر است',
                                                                           'max_length': '.شماره موبایل نامعتبر است'})
    password = forms.CharField(label=':رمز عبور', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.data
        print(cleaned_data)
        user = authenticate(mobile=cleaned_data['mobile'], password=cleaned_data['password'])
        if user is None:
            raise forms.ValidationError("متاسفانه کاربری با مشخصات داده‌شده پیدا نشد.")
        return cleaned_data
