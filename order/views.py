from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, TemplateView

from accounts.forms import AddressForm
from accounts.models import Address
from order.forms import OrderForm, OrderItemForm
from order.models import Order, OrderItem, Coupon


# Create your views here.
class AddOrderAddress(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'order/add-address.html'
    success_url = '/orders/create-order/'

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


class CreateOrder(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/create-order.html'
    success_url = '/orders/add-item/'

    def form_valid(self, form):
        form.instance.customer = self.request.user
        super().form_valid(form)
        return render(self.request, 'order/add-item.html', context={'order_id': self.object.id})


class AddOrderItem(LoginRequiredMixin, CreateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'order/add-item.html'
    success_url = '/orders/add-item/'


def order_result(request):
    if request.method == 'POST':
        try:
            user_coupon = Coupon.objects.get(code=request.POST['del-coupon'])
            user_coupon.customers.remove(request.user)
            user_coupon.save()
            return render(request, 'order/order-result.html')
        except (KeyError, Coupon.DoesNotExist):
            return render(request, 'order/order-result.html')
    return render(request, 'order/order-result.html')


class DetailOrder(DetailView):
    model = Order
    template_name = 'order/order-detail.html'


class ListOrder(ListView):
    model = Order
    context_object_name = 'carts'
    template_name = 'order/all_orders.html'
