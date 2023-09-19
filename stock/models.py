from django.db import models
from account.models import Account

# Create your models here.

class stock_type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Stock(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=50)
    stock_quantity = models.IntegerField()
    stock_type = models.ForeignKey(stock_type, on_delete=models.SET_NULL, null=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    stock_image= models.ImageField(upload_to= 'stocks_images')
    stock_item_size = models.IntegerField(null=True)

    
    def __str__(self):
        return self.stock_name


