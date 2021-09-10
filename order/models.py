from django.conf import settings
from django.db import models

# Create your models here.
from coupan.models import Coupon
from product.models import Product


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='orders')
    order_num = models.IntegerField(max_length=20)
    datetime = models.DateTimeField(auto_now_add=True)
    shipping_types = (('pishtaz', 'pishtaz'), ('sefareshi', 'sefareshi'))
    shipping = models.CharField(choices=shipping_types, max_length=20)
    status_code = (('1', 'cancel'),
                   ('2', 'success'),
                   ('3', 'process'),
                   ('4', 'deliver'),
                   ('5', 'send'),
                   ('6', 'active'))
    status = models.CharField(choices=status_code, max_length=20)

    def __str__(self):
        return self.order_num

    @classmethod
    def get_active_order(cls, user):
        return cls.objects.get_or_create(user=user, status='6')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.order}'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.RESTRICT)
    payment_statues = (('successful', 'successful'), ('failed', 'failed'))
    payment_info = models.CharField(choices=payment_statues, max_length=50)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order: {self.order}, datetime:{self.payment_info}'

    @property
    def final_amount(self):
        coupons = Coupon.objects.all()
        for coupon in coupons:
            if self.order.customer in coupon.customers.all():
                return int(self.amount - (self.amount * coupon.amount / 100))
