from django.contrib import admin
from order.models import Order, OrderItem, Coupon


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3
    max_num = 30


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'customer', 'shipping', 'datetime']
    search_fields = ['id', 'status', 'customer', 'shipping', ]
    inlines = [OrderItemInline, ]
    readonly_fields = ['datetime', 'customer', 'shipping', 'address', ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', ]
    search_fields = ['order', ]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', ]
    search_fields = ['code', 'amount', 'customers', ]
    filter_horizontal = ['customers', ]
