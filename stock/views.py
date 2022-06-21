from datetime import datetime, timedelta

from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max

from .models import Stock
from isis.models import Product
from warehouse.models import Warehouse

from .forms import StockSearchForm


# Create your views here.
@login_required
def stock_movement_view(request):
    stock = Stock.objects.all().order_by('-date_created')
    
    context = {}
    context['object_list'] = stock

    return render(request, 'stock/listviews/stock_movement.html', context) 


# Create your views here.
@login_required
def stock_item_list_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    stock = Stock.objects.filter(product=product).order_by('-date_created')
    
    context = {}
    context['object_list'] = stock
    context['product'] = product
    
    return render(request, 'stock/listviews/stock_item_list.html', context) 

def search_summary(start_date, end_date):
    
    p = Product.objects.raw("""SELECT p.*, (SELECT SUM(s.quantity) AS q FROM stock_stock AS s 
    WHERE s.product_id=p.id AND (s.date_created BETWEEN '{}' AND '{}' )) AS qt FROM isis_product AS p""".format(start_date, end_date))

    print(p.query)
    
    context = {}
    context['object_list'] = p

    return context


# Create your views here.
@login_required
def stock_summary_list_view(request):
    
    if request.method == 'POST':
        search_form = StockSearchForm(request.POST)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    else:
        search_form = StockSearchForm()
        _start_date = datetime.now() - timedelta(days=30)
        _end_date = datetime.now()
        start_date = _start_date
        end_date = _end_date

    context = search_summary(start_date, end_date)
    context['search_form'] = search_form

    return render(request, 'stock/listviews/stock_summary_list.html', context)


    