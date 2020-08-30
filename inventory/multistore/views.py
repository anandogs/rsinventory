from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse
from .forms import TransactForm
import pandas as pd
import numpy as np

from . models import Stock, SKU, Location

def index(request):

    context = {
        'stock_details' : Stock.objects.all()
    }
    return render(request, 'multistore/index.html', context)

def transact(request):
    if request.method == 'POST':
        form = TransactForm(request.POST)
    if form.is_valid():
        if 'returns' in request.POST:
            obj = form.save(commit=False)
            obj.quantity = -form.cleaned_data['quantity']
            obj.save()
        form.save()
        # return render(request, 'multistore/index.html')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def sale(request):


    form = TransactForm()
    context = {
        'form' : form,
        'form_type' : 'sales'
    }
    
    return render(request, 'multistore/form.html', context)

def transfer(request):
    return HttpResponse('transfer page')

@login_required(login_url='multistore/login/')
def returns(request):

    form = TransactForm()
    context = {
        'form' : form,
        'form_type' : 'returns'
    }
    
    return render(request, 'multistore/form.html', context)

def download(request):

    stock_list = Stock.objects.all()

    data_list = []

    for stock in stock_list:
        order_no = stock.order_no
        sku = stock.sku
        quantity = stock.quantity
        location = stock.location
        dict_to_append = {'Order Number':order_no, 'SKU':sku.sku_code, 'Quantity':quantity, 'Location':location.location_name}
        data_list.append(dict_to_append)

    df = pd.DataFrame(data_list)
    
    grouped_df = df.pivot_table(values='Quantity', index='SKU', columns='Location', aggfunc=np.sum).reset_index()
    
    grouped_df.to_excel('output.xlsx', index=False)

    return HttpResponse('transfer page')

def login_view(request):
    if request.method == 'POST':        
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            user = form.get_user()
            print(user)
            # user = authenticate(username=username, password=password)
            # print(user)
            login(request, user)
            return HttpResponseRedirect('/')
    form = AuthenticationForm()
    return render(request, 'multistore/login.html', {'form':form})
