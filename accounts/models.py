from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where mobile is the unique identifiers
    for authentication instead of username.
    """

    def create_user(self, mobile, password, **extra_fields):
        """
        Create and save a User with the given mobile and password.
        """
        if not mobile:
            raise ValueError(_('شماره موبایل وارد نشده!'))
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given mobile and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mobile, password, **extra_fields)


# Create your models here.

class Customer(AbstractUser):
    username = None
    mobile = models.CharField(_('شماره موبایل'), unique=True, max_length=11, )
    first_name = models.CharField(_('نام'), max_length=150)
    last_name = models.CharField(_('نام‌خانوادگی'), max_length=150)
    email = models.EmailField(_('ایمیل'), unique=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'مشتریان'
        verbose_name = 'مشتری'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',
                                 verbose_name=_('کاربر'))
    province = models.CharField(_('استان'), max_length=200)
    city = models.CharField(_('شهر'), max_length=200)
    exact_address = models.TextField(_('آدرس دقیق'), )
    apartment_number = models.PositiveSmallIntegerField(_('پلاک'), )
    unit = models.PositiveSmallIntegerField(_('واحد'), blank=True, null=True)
    zip_code = models.PositiveIntegerField(_('کدپستی'), blank=True, null=True)

    def __str__(self):
        return f'{self.city} - {self.exact_address}'

    class Meta:
        verbose_name_plural = 'آدرس‌ها'
        verbose_name = 'آدرس'
