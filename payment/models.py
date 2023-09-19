from django.db import models
from account.models import Account

# Create your models here.
payment_type_choice = [
    ('ussd','ussd'),
    ('bank-card', 'bank-card'),
    ('bank-transfer', 'bank-transfer')
]
payment_plan_choice = [
    ('Monthly','Monthly'),
    ('6-month', '6-month'),
    ('Yearly', 'Yearly')
]
class payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment_id= models.CharField(max_length=30, null=True)
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=50, null=True, choices=payment_type_choice)
    payment_plan = models.CharField(max_length=50, null=True, choices=payment_plan_choice)
    date = models.DateTimeField()

    
    def __str__(self):
        return self.user.username

class Subscription(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField(null=True)  

    def __str__(self):
        return self.user.username  