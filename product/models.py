from django.core.validators import MaxValueValidator
from django.db import models
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


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, unique=True)
    # main image
    image = models.ImageField(upload_to=product_image_path)
    description = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
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
                return int(self.price - (self.price * discount.amount / 100))
        return self.price


class ProductMedia(models.Model):
    # product additional media like: additional images, videos,...
    image = 'image'
    video = 'video'
    media_types = (
        (image, 'image'),
        (video, 'video')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    media = models.FileField(choices=media_types, upload_to=product_media_path)

    class Meta:
        verbose_name_plural = 'مدیاهای محصولات'
        verbose_name = 'مدیا'

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
