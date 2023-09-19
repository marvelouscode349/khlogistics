from django.contrib import admin

from . models import Order, order_complete

admin.site.register(Order)
admin.site.register(order_complete)
# Register your models here.
