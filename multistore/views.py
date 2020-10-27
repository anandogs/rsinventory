from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .forms import TransactForm, TransferForm
import pandas as pd
import numpy as np
from io import BytesIO as IO

from . models import Stock, SKU, Location

def index(request):
    if 'term' in request.GET:
        qs = SKU.objects.filter(sku_code__icontains=request.GET.get('term'))
        skus = list()
        for sku in qs:
            skus.append(sku.sku_code)
        return JsonResponse(skus, safe=False)
    td = datetime.today()
    mnth = td.month
    context = {
        'stock_details' : Stock.objects.filter(timestamp__month=mnth).exclude(order_no='Upload')
    }
    return render(request, 'multistore/index.html', context)


def check_inv(sku, inv, loc):
    '''gets sku and location object and checks if total quantity is less than 0 and returns True if inv is positive and False if negative'''
    sku_obj = SKU.objects.get(sku_code=sku)
    loc_obj = Location.objects.get(location_name=loc)
    stock_data = Stock.objects.filter(sku=sku_obj, location=loc_obj)
    qty = 0
    for stock in stock_data:
        qty = qty + stock.quantity

    qty = qty + inv
    if qty >= 0:
        return True
    return False


def transact(request):
    if request.method == 'POST':
        current_user = request.user
        form = TransactForm(request.POST)
        
        if form.is_valid():
            order_no =  form.cleaned_data['order_no']
            user_sku = form.cleaned_data['sku']
            user_loc = form.cleaned_data['location']
            try:
                sku = SKU.objects.get(sku_code=user_sku)
            except ObjectDoesNotExist:
                return HttpResponse("ERROR INCORRECT SKU. PLEASE GO BACK AND TRY AGAIN")
            loc = Location.objects.get(location_name=user_loc)
            qty = form.cleaned_data['quantity']
            if 'sale' in request.POST:
                qty = -qty
                
            res = check_inv(sku, qty, loc)
            print(res)
            if res:
                transaction = Stock.objects.create(order_no=order_no, sku=sku, quantity=qty, location=loc, user=current_user)

                transaction.save()
            else:
                return HttpResponse("ERROR-NEGATIVE QUANTITY TRANSACTION CANCELLED. PLEASE GO BACK AND TRY AGAIN")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def sale(request):

    form = TransactForm()
    context = {
        'form' : form,
        'form_type' : 'sale',
    }
    
    return render(request, 'multistore/form.html', context)

@login_required(login_url='login')
def transfer(request):

    if request.method == 'POST':
        current_user = request.user
        form = TransferForm(request.POST)
        if form.is_valid():
            sku = form.cleaned_data['sku']
            to_quantity = form.cleaned_data['quantity']
            from_quantity = -to_quantity
            loc_from = form.cleaned_data['location_from']
            loc_to = form.cleaned_data['location_to']

            try:
                sku = SKU.objects.get(sku_code=sku)
            except ObjectDoesNotExist:
                return HttpResponse("ERROR INCORRECT SKU. PLEASE GO BACK AND TRY AGAIN")

            res = check_inv(sku, from_quantity, loc_from)
            if res:

            # transaction #1
                transaction1 = Stock.objects.create(order_no='Transfer', sku=sku, quantity=to_quantity, location=loc_to, user=current_user)
                transaction2 = Stock.objects.create(order_no='Transfer', sku=sku, quantity=from_quantity, location=loc_from, user=current_user)
                
                transaction1.save()
                transaction2.save()
            else:
                    return HttpResponse("ERROR-NEGATIVE QUANTITY TRANSACTION CANCELLED. PLEASE GO BACK AND TRY AGAIN")

    form = TransferForm()
    context = {
        'form' : form,
        'form_type' : 'transfer'
    }
    
    return render(request, 'multistore/form.html', context)
    

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
    
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    grouped_df.to_excel(xlwriter, sheet_name='inventory', index=False)
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rs_inventory.xlsx'
    return response


    # context = {
    #     'stock_details' : Stock.objects.all()
    # }
    # return render(request, 'multistore/index.html', context)

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


def upload_sku(request):
    user = request.user
    df = pd.read_excel('/Users/anandoghose/Desktop/products.xlsx')
    df = df['SKU']
    for i in range(len(df)):
        sku_code = df.loc[i]
        print(sku_code)
        sku_list = SKU.objects.create(sku_code=sku_code)
        sku_list.save()

    

def upload_file(request):
    user = request.user
    df = pd.read_excel('/Users/anandoghose/Desktop/products.xlsx')

    #create SKUs first

    df['SKU'].dropna(inplace=True)
    df['SKU'].drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)

    for col in df.columns:
        try:
            location = Location.objects.get(location_name=col)
            print(col)
            for i in range(len(df)):
                if df.loc[i,col] == 0:
                    pass
                else:
                    quantity = df.loc[i,col]
                    sku_code = df.loc[i,'SKU']
                    # print(sku_code)
                    sku = SKU.objects.get(sku_code=sku_code)
                    transaction = Stock.objects.create(order_no='Upload', sku=sku, quantity=quantity, location = location, user=user)
                    transaction.save()

        except Location.DoesNotExist:
            
            print (f'warning the following column does not have a location allocated to it: {col}')
    
    return HttpResponse('Done')
