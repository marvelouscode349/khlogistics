from django import forms

from . models import Stock

class AddStock(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_name', 'stock_quantity', 'stock_type', 'stock_image', 'stock_item_size']