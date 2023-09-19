from django.db import models
from stock.models import Stock
from account.models import Account

from django.utils import timezone

# Create your models here
LOCAL_GOVERNMENT_CHOICES = [
    ('agege', 'Agege'),
    ('ajeromi-ifelodun', 'Ajeromi-Ifelodun'),
    ('alimosho', 'Alimosho'),
    ('amuwo-odofin', 'Amuwo-Odofin'),
    ('apapa', 'Apapa'),
    ('badagry', 'Badagry'),
    ('epe', 'Epe'),
    ('Eti-Osa', 'Eti-Osa'),
    ('ibeju-lekki', 'Ibeju-Lekki'),
    ('ifako-ijaiye', 'Ifako-Ijaiye'),
    ('ikeja', 'Ikeja'),
    ('ikorodu', 'Ikorodu'),
    ('kosofe', 'Kosofe'),
    ('lagos-island', 'Lagos Island'),
    ('lagos-mainland', 'Lagos Mainland'),
    ('mushin', 'Mushin'),
    ('ojo', 'Ojo'),
    ('oshodi-isolo', 'Oshodi-Isolo'),
    ('somolu', 'Somolu'),
    ('surulere', 'Surulere'),
]

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    rider = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='rider')
    order_name = models.CharField(max_length=50)
    order_la = models.CharField(max_length=50, choices=LOCAL_GOVERNMENT_CHOICES, null=True)
    address = models.CharField(max_length=50)
   
    order_quantity = models.IntegerField()
    order_size = models.IntegerField(null=True)

    order_price = models.IntegerField(null=True)
    
    recipient_number = models.CharField(max_length=50)
    date = models.DateTimeField()
    status = models.CharField( max_length=50, default = 'uncomplete')
    
    def save(self, *args, **kwargs):
        if not self.id and not self.date:
            self.date = timezone.localtime(timezone.now())
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_name

class order_complete(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_complete_image = models.ImageField(upload_to='order_complete')

    def __str__(self):
        return self.order.order_name



