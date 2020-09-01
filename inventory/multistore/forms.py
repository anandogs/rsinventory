from django import forms
from django.forms import ModelForm, TextInput
from multistore.models import Stock, Location, SKU

class TransactForm(ModelForm):
    class Meta:
        
        model = Stock
        fields = ['order_no', 'sku', 'quantity', 'location']

class TransferForm(forms.Form):
    sku = forms.ModelChoiceField(queryset=SKU.objects.all())
    quantity = forms.IntegerField()
    location_from  = forms.ModelChoiceField(queryset=Location.objects.all())
    location_to = forms.ModelChoiceField(queryset=Location.objects.all())
    

