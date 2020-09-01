from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import pandas as pd
import numpy as np

from . models import Stock, SKU, Location

def index(request):

    if 'term' in request.GET:
        inv = SKU.objects.filter(sku_code__istartswith=request.GET.get('term'))
        
        output = list()
        for product in inv:
            output.append(product.sku_code)
        return JsonResponse(output, safe=False)


    context = {
        'stock_details' : Stock.objects.all()
    }
    return render(request, 'multistore/index.html', context)


def sale(request):
    
    if request.method=='POST':
        order_id = request.POST['order']
        sku = request.POST['sku']
        sku_returned = SKU.objects.get(sku_code = sku)
        quantity = -int(request.POST['quantity'])
        location = request.POST['location']
        location_returned = Location.objects.get(location_name=location)

        Stock.objects.create(order_no=order_id, sku=sku_returned, quantity=quantity, location=location_returned)
        return HttpResponseRedirect(reverse('sale'))
    
    context = {
        'locations' : Location.objects.all()
    }
    return render(request, 'multistore/sale.html', context)

def transfer(request):
    return HttpResponse('transfer page')

def returns(request):
    if request.method=='POST':
        order_id = request.POST['order']
        sku = request.POST['sku']
        sku_returned = SKU.objects.get(sku_code = sku)
        quantity = int(request.POST['quantity'])
        location = request.POST['location']
        location_returned = Location.objects.get(location_name=location)

        Stock.objects.create(order_no=order_id, sku=sku_returned, quantity=quantity, location=location_returned)
        return HttpResponseRedirect(reverse('returns'))
    
    context = {
        'locations' : Location.objects.all()
    }
    return render(request, 'multistore/returns.html', context)

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
