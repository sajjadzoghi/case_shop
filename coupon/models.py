from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
class Coupon(models.Model):
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='coupons')
    code = models.CharField(max_length=15)
    amount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name_plural = 'کدهای تخفیف'
        verbose_name = 'کد تخفیف'

    def __str__(self):
        return f'{self.code} - {self.amount}%'
