from django import forms
from django.forms import ModelForm, TextInput
from multistore.models import Stock

class TransactForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['order_no', 'sku', 'quantity', 'location']
