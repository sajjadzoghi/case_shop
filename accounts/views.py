from django.contrib.auth import login, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.forms import LoginForm

Customer = get_user_model()


# Create your views here.

def login_view(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login(request, Customer.objects.get(mobile=login_form.cleaned_data['mobile']))
            if 'next' in request.GET:
                HttpResponseRedirect(request.GET['next'])
            return redirect('product:all_product')

    return render(request, 'base/base.html', context={
        'login_form': login_form
    })
