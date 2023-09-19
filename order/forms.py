from django import forms
from . models import Order, order_complete
from stock.models import Stock
from account.models import Account

class AddOrder(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['stock', 'order_name', 'address', 'order_quantity', 'recipient_number', 'order_la','order_price']
        widgets = {
            'order_price':forms.TextInput(attrs={'readonly': 'readonly', 'placeholder':'Price', 'style':'background-color: #2A3038;'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        # Remove 'user' from kwargs
        super().__init__(*args, **kwargs)
        if user:
            self.fields['stock'].queryset = Stock.objects.filter(is_approved=True, user=user)

        

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class order_complete(forms.ModelForm):
    class Meta:
        model = order_complete
        fields = ['order_complete_image']

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
       


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
  