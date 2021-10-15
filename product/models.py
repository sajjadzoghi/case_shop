from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg, Count
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from shop.utils import product_image_path


# Create your models here.
class Category(models.Model):
    name = models.CharField(_('عنوان'), max_length=30, unique=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='children', verbose_name=_('دسته بندی پدر'))
    icon = models.CharField(_('آیکون فونت'), max_length=30)

    class Meta:
        verbose_name_plural = 'دسته‌بندی‌ها'
        verbose_name = 'دسته‌بندی'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(_('نام رنگ'), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'رنگ‌ها'
        verbose_name = 'رنگ'

    def __str__(self):
        return self.name


# product additional media: video or additional images
class ProductMedia(models.Model):
    name = models.CharField(_('نام محصول موردنظر'), max_length=150)
    image = models.ImageField(_('بارگزاری تصویر محصول'), upload_to=product_image_path)
    date_created = models.DateTimeField(_('تاریخ بارگزاری تصویر'), auto_now_add=True)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'عکس‌های محصولات'
        verbose_name = 'عکس محصول'

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    image_tag.short_description = 'Image'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('دسته بندی'))
    name_fa = models.CharField(_('نام فارسی'), max_length=200, unique=True)
    name_en = models.CharField(_('نام انگلیسی'), max_length=200, unique=True)
    images = models.ManyToManyField(ProductMedia, blank=True, related_name='products', verbose_name=_('تصاویر'))
    description = models.TextField(_('توضیحات محصول'), )
    colors = models.ManyToManyField(Color, blank=True, related_name='products', verbose_name=_('رنگ‌ها'))
    inventory = models.IntegerField(_('موجودی'), default=0)
    price = models.IntegerField(_('قیمت (به تومان)'), )
    date_created = models.DateTimeField(_('تاریخ ایجاد محصول'), auto_now_add=True)

    class Meta:
        ordering = ['date_created']
        verbose_name_plural = 'محصولات'
        verbose_name = 'محصول'

    def __str__(self):
        return self.name_fa

    @property
    def final_price(self):
        discounts = ProductDiscount.objects.all()
        for discount in discounts:
            if self in discount.products.all():
                return int(self.price - (self.price * discount.amount / 100))
        return self.price

    @property
    def voters_number(self):
        product = Product.objects.filter(id=self.id).annotate(voters_num=Count('rates'))
        return product[0].voters_num

    @property
    def rate_average(self):
        product = Product.objects.filter(id=self.id).annotate(rates_avg=Avg('rates'))
        if not product[0].rates_avg:
            return 0
        return product[0].rates_avg


# Each product has its especial guarantees.
class Guarantee(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='guarantees',
                                verbose_name=_('محصول موردنظر'))
    name = models.CharField(_('عنوان گارانتی'), max_length=200)
    amount = models.IntegerField(_('قیمت (به تومان)'), )

    class Meta:
        verbose_name_plural = 'گارانتی مجصولات'
        verbose_name = 'گارانتی'

    def __str__(self):
        return self.name


class ProductDiscount(models.Model):
    products = models.ManyToManyField(Product, related_name='discounts', verbose_name=_('محصولات موردنظر'))
    amount = models.PositiveSmallIntegerField(_('درصد تخفیف'), validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name_plural = 'تخفیفات کلی محصولات'
        verbose_name = 'تخفیف'

    def __str__(self):
        return f'{self.amount}%'


class ProductRate(models.Model):
    # rate levels:
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    rate_levels = (
        (one, 1),
        (two, 2),
        (three, 3),
        (four, 4),
        (five, 5),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates',
                                verbose_name=_('محصول موردنظر'))
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='rates',
                                 verbose_name=_('امتیاز دهنده'))
    rate_level = models.IntegerField(_('امتیاز'), choices=rate_levels)

    class Meta:
        verbose_name_plural = 'امتیازات محصولات'
        verbose_name = 'امتیاز محصول'

    def __str__(self):
        return f'{self.product}, {self.customer}, {self.rate_level}'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',
                                verbose_name=_('محصول موردنظر'))
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='comments',
                                 verbose_name=_('نظر دهنده'))
    text = models.TextField(_('متن نظر (یا دیدگاه)'), )

    class Meta:
        verbose_name_plural = 'نظرات محصولات'
        verbose_name = 'نظر درباره محصول'

    def __str__(self):
        return f'{self.product}, {self.customer}'
