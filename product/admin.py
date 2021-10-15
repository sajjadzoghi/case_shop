from django.contrib import admin
from product.models import (Category, Product, Color, ProductMedia, ProductDiscount, Guarantee, ProductRate,
                            ProductComment)

# Register your models here.
admin.site.register(Color)
admin.site.register(ProductRate)
admin.site.register(ProductComment)


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1
    max_num = 30


class GuaranteeInline(admin.TabularInline):
    model = Guarantee
    extra = 2
    max_num = 10


class ProductDiscountInline(admin.StackedInline):
    model = ProductDiscount.products.through
    extra = 1
    max_num = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    search_fields = ['name', ]
    inlines = [ProductInline, ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_fa', 'price', 'inventory']
    search_fields = ['name_fa', ]
    filter_horizontal = ['images', ]
    readonly_fields = ['date_created', ]
    inlines = [GuaranteeInline, ProductDiscountInline]


@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'amount', ]
    search_fields = ['product', ]


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag', ]
    fields = ['name', 'image', 'image_tag', ]
    readonly_fields = ['image_tag', ]
    search_fields = ['name', ]


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    search_fields = ['products__name', ]
