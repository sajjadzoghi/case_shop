from django.conf import settings
from django.db import models

# Create your models here.
from coupon.models import Coupon
from product.models import Product


class Order(models.Model):
    # shipping types
    pishtaz = 'پیشتاز'
    sefareshi = 'سفارشی'
    shipping_types = ((pishtaz, 'پیشتاز'), (sefareshi, 'سفارشی'))

    # order status
    cancel = 'انصراف'
    active = 'فعال'
    bargiri = 'بارگیری'
    delivery = 'پیک'
    sent = 'تحویل'
    order_status = (
        (cancel, 'انصراف'),
        (active, 'فعال'),
        (bargiri, 'پرداخت موفق و درحال بارگیری از انبار'),
        (delivery, 'درحال ارسال توسط پیک'),
        (sent, 'تحویل سفارش به مشتری'),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='orders')
    datetime = models.DateTimeField(auto_now_add=True)
    shipping = models.CharField(choices=shipping_types, max_length=10, default=sefareshi)
    status = models.CharField(choices=order_status, max_length=20)

    class Meta:
        verbose_name_plural = 'سفارش‌ها'
        verbose_name = 'سفارش'

    def __str__(self):
        return f'سفارش: {self.id}, وضعیت مرسوله: {self.status}'

    @property
    def total_without_coupon(self):
        return sum([item.total_item_price for item in self.items.all()])

    @property
    def total_with_coupon(self):
        coupon = Coupon.objects.get(customers__mobile=self.customer.mobile)
        if coupon:
            return int(self.total_without_coupon - (self.total_without_coupon * coupon.amount / 100))

    def total_order_price(self):
        self.items.total_item_price * len(self.items.all())

    @classmethod
    def get_active_order(cls, customer):
        return cls.objects.get_or_create(customer=customer, status=cls.active)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'محصولات هر سفارش'
        verbose_name = 'محصول در یک سفارش'

    def __str__(self):
        return f'{self.order}'

    @property
    def total_item_price(self):
        return self.quantity * self.product.final_price


class Payment(models.Model):
    # payment status
    successful = 'موفق'
    failed = 'ناموفق'
    payment_status = ((successful, 'موفق'), (failed, 'ناموفق'))

    order = models.OneToOneField(Order, on_delete=models.RESTRICT, related_name='payment')
    status = models.CharField(choices=payment_status, max_length=50)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'پرداخت‌ها'
        verbose_name = 'پرداخت'

    def __str__(self):
        return f'سفارش: {self.order}, وضعیت پرداخت: {self.status}'
