from django.conf import settings
from django.db import models


# Create your models here.
class Coupon(models.Model):
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='coupons')
    code = models.CharField(max_length=15)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.code} - {self.amount}%'
