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
    readonly_fields = ['first_name', 'last_name', 'mobile', 'email', 'password']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'exact_address', ]
    search_fields = ['customer', 'city']
    readonly_fields = ['customer', 'province', 'city', 'exact_address', 'apartment_number', 'unit', 'zip_code', ]
