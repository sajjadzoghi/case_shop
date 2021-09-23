from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from order.models import Order, OrderItem


# Create your views here.
# -------------- Order Views ----------------------
class DetailOrder(DetailView):
    model = Order
    template_name = 'cart/detail_cart.html'


class ListOrder(ListView):
    model = Order
    context_object_name = 'carts'
    template_name = 'cart/list_carts.html'


class CreateOrder(CreateView):
    model = Order
    template_name = 'cart/create_cart.html'


class Updatecart(UpdateView):
    model = Order
    template_name = 'cart/update_cart.html'


class DeleteOrder(DeleteView):
    model = Order
    template_name = 'cart/delete_cart.html'


# -------------- OrderItem Views -------------------
class DetailOrderItem(DetailView):
    model = OrderItem
    template_name = 'cartitem/detail_cartitem.html'


class ListOrderItem(ListView):
    model = OrderItem
    context_object_name = 'cartitems'
    template_name = 'cartitem/list_cartitems.html'


class CreateItemOrder(CreateView):
    model = OrderItem
    template_name = 'cartitem/create_cartitem.html'


class UpdateOrderItem(UpdateView):
    model = OrderItem
    template_name = 'cartitem/update_cartitem.html'


class DeleteOrderItem(DeleteView):
    model = Order
    template_name = 'cartitem/delete_cartitem.html'
