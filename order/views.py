from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from order.models import Order


# Create your views here.
class CreateOrder(CreateView):
    model = Order
    template_name = 'order/create_cart.html'


class DetailOrder(DetailView):
    model = Order
    template_name = 'order/detail_cart.html'


class ListOrder(ListView):
    model = Order
    context_object_name = 'carts'
    template_name = 'order/list_carts.html'


class DeleteOrder(DeleteView):
    model = Order
    template_name = 'order/delete_cart.html'
