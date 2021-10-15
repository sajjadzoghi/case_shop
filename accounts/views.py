from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from accounts.forms import LoginForm, ProfileForm, ImageForm
from order.models import Order

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


@login_required
def profile_view(request):
    profile_form = ProfileForm(instance=request.user)
    image_form = ImageForm(instance=request.user)
    if request.method == 'POST' and 'send-profile' in request.POST:
        print(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:profile')
    elif request.method == 'POST' and 'send-img' in request.POST:
        image_form = ImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', context={'profile_form': profile_form,
                                                             'image_form': image_form, })


class OrdersHistoryView(LoginRequiredMixin, ListView):
    template_name = 'accounts/orders-history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
