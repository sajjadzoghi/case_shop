from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


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
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.TextField()
    apartment_number = models.PositiveSmallIntegerField()
    zip_code = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.customer.last_name} ,{self.city}'

    class Meta:
        verbose_name_plural = 'آدرس‌ها'
        verbose_name = 'آدرس'
