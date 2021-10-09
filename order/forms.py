from django import forms
from order.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping', 'address', ]
        widgets = {
            'shipping': forms.Select(attrs={'class': 'form-control col-5'}),
        }
        error_messages = {
            'address': {'required': '.آدرس انتخاب نشده'}
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
