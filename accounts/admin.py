from django.contrib import admin

# Register your models here.
from accounts.models import Customer

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Customer)