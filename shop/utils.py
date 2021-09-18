def product_image_path(instance, filename):
    name = filename.split('.')
    return f'{instance.category}/product-{instance.id}/{hash(name[0])}.{name[-1]}'


def product_media_path(instance, filename):
    name = filename.split('.')
    return f'{instance.product.category}/product-{instance.product.id}/{hash(name[0])}.{name[-1]}'
