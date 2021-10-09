from django.contrib import admin
from accounts.models import Customer, Address


# Register your models here.

class AddressInline(admin.StackedInline):
    model = Address
    extra = 2
    max_num = 20


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'mobile', 'email', ]
    search_fields = ['last_name', 'mobile', ]
    inlines = [AddressInline, ]


@admin.register(Address)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'exact_address', ]
    search_fields = ['customer', 'city']
