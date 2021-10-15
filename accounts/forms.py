from django.contrib.auth import authenticate
from django import forms

from accounts.models import Address, Customer


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


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['mobile'].widget.attrs['readonly'] = True

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'mobile', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('image', )