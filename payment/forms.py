from django import forms
from . models import payment


class AddPayment(forms.ModelForm):
    class Meta:
        model = payment
        fields = ['payment_plan','amount','payment_type',]