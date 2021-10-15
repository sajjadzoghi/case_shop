from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from order.forms import OrderForm, OrderItemForm
from order.models import Order, OrderItem, Coupon


# Create your views here.

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
