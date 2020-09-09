from django import forms
from django.forms import ModelForm, TextInput
from multistore.models import Stock, Location, SKU

class TransactForm(forms.Form):
    sku = forms.CharField()
    quantity = forms.IntegerField()
    location  = forms.ModelChoiceField(queryset=Location.objects.all())
    
class TransferForm(forms.Form):
    sku = forms.CharField()
    quantity = forms.IntegerField()
    location_from  = forms.ModelChoiceField(queryset=Location.objects.all())
    location_to = forms.ModelChoiceField(queryset=Location.objects.all())
    
    

