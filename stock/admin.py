from django.contrib import admin
from . models import Stock, stock_type

# Register your models here.
admin.site.register(Stock)
admin.site.register(stock_type)