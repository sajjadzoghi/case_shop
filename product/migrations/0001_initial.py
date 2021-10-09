# Generated by Django 3.2.5 on 2021-10-05 21:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shop.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='عنوان')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='دسته بندی پدر')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='نام رنگ')),
            ],
            options={
                'verbose_name': 'رنگ',
                'verbose_name_plural': 'رنگ\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_fa', models.CharField(max_length=200, unique=True, verbose_name='نام فارسی')),
                ('name_en', models.CharField(max_length=200, unique=True, verbose_name='نام انگلیسی')),
                ('description', models.TextField(verbose_name='توضیحات محصول')),
                ('inventory', models.IntegerField(default=0, verbose_name='موجودی')),
                ('price', models.IntegerField(verbose_name='قیمت (به تومان)')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category', verbose_name='دسته بندی')),
                ('colors', models.ManyToManyField(blank=True, related_name='products', to='product.Color', verbose_name='رنگ\u200cها')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام محصول موردنظر')),
                ('image', models.ImageField(upload_to=shop.utils.product_image_path, verbose_name='بارگزاری تصویر محصول')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بارگزاری تصویر')),
            ],
            options={
                'verbose_name': 'عکس محصول',
                'verbose_name_plural': 'عکس\u200cهای محصولات',
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='ProductRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='امتیاز')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='rates', to=settings.AUTH_USER_MODEL, verbose_name='امتیاز دهنده')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='product.product', verbose_name='محصول موردنظر')),
            ],
            options={
                'verbose_name': 'امتیاز محصول',
                'verbose_name_plural': 'امتیازات محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('products', models.ManyToManyField(related_name='discounts', to='product.Product', verbose_name='محصولات موردنظر')),
            ],
            options={
                'verbose_name': 'تخفیف',
                'verbose_name_plural': 'تخفیفات کلی محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن نظر (یا دیدگاه)')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='نظر دهنده')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product.product', verbose_name='محصول موردنظر')),
            ],
            options={
                'verbose_name': 'نظر درباره محصول',
                'verbose_name_plural': 'نظرات محصولات',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.ProductMedia', verbose_name='تصاویر'),
        ),
        migrations.CreateModel(
            name='Guarantee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='عنوان گارانتی')),
                ('amount', models.IntegerField(verbose_name='قیمت (به تومان)')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guarantees', to='product.product', verbose_name='محصول موردنظر')),
            ],
            options={
                'verbose_name': 'گارانتی',
                'verbose_name_plural': 'گارانتی مجصولات',
            },
        ),
    ]
