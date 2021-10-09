from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from accounts.forms import LoginForm
from accounts.models import Address

Customer = get_user_model()


# Create your views here.

def login_view(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login(request, Customer.objects.get(mobile=login_form.cleaned_data['mobile']))
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('product:all_products')

    return render(request, 'accounts/login.html', context={
        'login_form': login_form
    })


def logout_view(request):
    logout(request)
    return redirect('product:all_products')


# class AddAddress(LoginRequiredMixin, CreateView):
#     model = Address
#     form_class = AddressForm
#     template_name = 'order/create-order.html'
#     success_url = '/order/order-result/'
#
#     def form_valid(self, form):
#         form.instance.customer = self.request.user
#         return super().form_valid(form)
