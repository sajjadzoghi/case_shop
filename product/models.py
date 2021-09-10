from django.db import models
from shop.utils import product_image_path1, product_image_path2


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='children')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # main image
    image = models.ImageField(upload_to=product_image_path1)
    description = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    inventory = models.IntegerField(default=0)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        discounts = ProductDiscount.objects.all()
        for discount in discounts:
            if self in discount.products.all():
                return int(self.price - (self.price * discount.amount / 100))


class ProductImage(models.Model):
    # additional image/images
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path2)

    def __str__(self):
        return self.product.name


class ProductDiscount(models.Model):
    products = models.ManyToManyField(Product, related_name='discounts')
    amount = models.IntegerField

    def __str__(self):
        return f'{self.amount}%'
