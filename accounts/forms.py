from django.contrib.auth import authenticate
from django import forms


class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.data
        user = authenticate(mobile=cleaned_data['mobile'], password=cleaned_data['password'])
        if user is None:
            raise forms.ValidationError("متاسفانه کاربری با مشخصات داده‌شده پیدا نشد.")
        return cleaned_data