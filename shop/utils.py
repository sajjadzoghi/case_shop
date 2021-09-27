import threading

from django.core.mail import send_mail


def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category/product-<name>/<filename>
    return f'{instance.category.name}/product-{instance.name}/{filename}'


def product_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category/product-<name>/<filename>
    return f'{instance.product.category.name}/product-{instance.product.name}/{filename}'


class EmailThreading(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            'kalashop@gmail.com',
            self.recipient_list,
            fail_silently=False
        )


def send_reset_password_mail(subject, message, recipient_list):
    EmailThreading(subject, message, recipient_list).start()
