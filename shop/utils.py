def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category/product-<name>/<filename>
    return f'{instance.category.name}/product-{instance.name}/{filename}'


def product_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category/product-<name>/<filename>
    return f'{instance.product.category.name}/product-{instance.product.name}/{filename}'
