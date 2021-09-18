from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg

from shop.utils import product_image_path, product_media_path


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='children')

    class Meta:
        verbose_name_plural = 'دسته‌بندی‌ها'
        verbose_name = 'دسته‌بندی'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'رنگ‌های مجصولات'
        verbose_name = 'رنگ'

    def __str__(self):
        return self.name


class Guarantee(models.Model):
    name = models.CharField(max_length=200, unique=True)
    amount = models.IntegerField()

    class Meta:
        verbose_name_plural = 'گارانتی مجصولات'
        verbose_name = 'گارانتی'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, unique=True)
    # main image
    image = models.ImageField(upload_to=product_image_path)
    description = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    guarantee = models.ForeignKey(Guarantee, on_delete=models.CASCADE, null=True)
    inventory = models.IntegerField(default=0)
    price = models.IntegerField()

    class Meta:
        verbose_name_plural = 'محصولات'
        verbose_name = 'محصول'

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        discounts = ProductDiscount.objects.all()
        for discount in discounts:
            if self in discount.products.all():
                f_price = int(self.price - (self.price * discount.amount / 100))
                if self.guarantee:
                    return f_price + self.guarantee.amount
                else:
                    return f_price
        return self.price

    @property
    def product_total_rate(self):
        product = self.annotate(rates_average=Avg('product_rate'))
        return product.rates_average


class ProductMedia(models.Model):
    # product additional media: video or additional images
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_media_path)
    video = models.FileField(upload_to=product_media_path)

    class Meta:
        verbose_name_plural = 'مدیاهای محصولات'
        verbose_name = 'مدیای محصول'

    def __str__(self):
        return self.product.name


class ProductDiscount(models.Model):
    products = models.ManyToManyField(Product, related_name='discounts')
    amount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='rates')
    rate_level = models.IntegerField(choices=rate_levels)

    class Meta:
        verbose_name_plural = 'امتیازات محصولات'
        verbose_name = 'امتیاز محصول'

    def __str__(self):
        return f'{self.product}, {self.customer}, {self.rate_level}'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='comments')
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'نظرات محصولات'
        verbose_name = 'نظر درباره محصول'

    def __str__(self):
        return f'{self.product}, {self.customer}'
