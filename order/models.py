from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator

from accounts.models import Address
from product.models import Product
from django.utils.translation import ugettext as _


# Create your models here.
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
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='orders',
                                 verbose_name=_('کاربر'))
    datetime = models.DateTimeField(_('تاریخ '), auto_now_add=True)
    shipping = models.CharField(_('نوع پست'), choices=shipping_types, max_length=20, default=sefareshi)
    status = models.CharField(_('وضعیت'), choices=order_status, max_length=20, default=bargiri)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name='orders', verbose_name=_('آدرس'))

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

    @classmethod
    def get_active_order(cls, customer):
        return cls.objects.get_or_create(customer=customer, status=cls.active)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('سفارش'))
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(_('تعداد'), )

    class Meta:
        verbose_name_plural = 'آیتم‌های سفارش'
        verbose_name = 'آیتم سفارش'

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    @property
    def total_item_price(self):
        return self.quantity * self.product.final_price


class Coupon(models.Model):
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='coupons',
                                       verbose_name=_('کاربران موردنظر'))
    code = models.CharField(_('کد تخفیف'), max_length=15)
    amount = models.PositiveSmallIntegerField(_('درصد تخفیف'), validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name_plural = 'کدهای تخفیف'
        verbose_name = 'کد تخفیف'

    def __str__(self):
        return f'{self.code} - {self.amount}%'
