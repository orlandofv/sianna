import datetime
import json
from math import prod

from django.db import connection, IntegrityError
from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import (Gallery, Product, Tax, Warehouse)
from users.models import User
from .forms import (ProductForm, TaxForm, WarehouseForm)
from django.contrib import messages #import messages
from django.utils.translation import ugettext_lazy as _
from config.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings

from config import utilities

@login_required
def product_list_view(request):
    product = Product.objects.all()
    context = {}
    context['object_list'] = product

    return render(request, 'isis/listviews/product_list.html', context) 

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        tax_form = TaxForm(request.POST)
        warehouse_form = WarehouseForm(request.POST)
        
        if form.is_valid() or tax_form.is_valid() or warehouse_form.is_valid():
            if request.POST.get('save_tax') or request.POST.get('save_tax_new'):
                instance = tax_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:product_create')
            
            if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:product_create')
            
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            
            parent = request.POST.get('parent')
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent
                
            product = instance
            instance = instance.save()
            
            slug = slugify(product.name)
            
            messages.success(request, _("Product added successfully!"))

            if request.POST.get('save_product'):
                return redirect('isis:product_details', slug=slug)
            else:
                return redirect('isis:product_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:product_create')
    else:
        form = ProductForm()
        tax_form = TaxForm()
        warehouse_form = WarehouseForm()
        
        context = {'form': form, 'tax_form': tax_form, 'warehouse_form': warehouse_form}
        return render(request, 'isis/createviews/product_create.html', context)


def get_model_name_from_id(model, id):
    try:
        product = model.objects.get(id=id)
        return product.name
    except Product.DoesNotExist:
        return None

@login_required
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=product)
    tax_form = TaxForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            
            parent = request.POST.get('parent')
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent

                # Since parent returns the product id we need to get the name of the parent product
                parent_name =  get_model_name_from_id(Product, parent)
                
                # If the updated product is same as parent
                if parent_name == product.name:
                    print('Same product')
                    instance.parent = 0

            instance = instance.save()
            messages.success(request, _("Product updated successfully!"))

            if request.POST.get('save_product'):
                return redirect('isis:product_details', slug=slug)
            else:
                return redirect('isis:product_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:product_update', slug=slug)
       
    context = {'form': form, 'tax_form': tax_form, 'warehouse_form': warehouse_form,}
    return render(request, 'isis/updateviews/product_update.html', context)


@login_required
def product_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Product.objects.filter(id__in=selected_ids).delete()
                    # Set parent to No parent in products with deleted parents
                    Product.objects.filter(parent__in=selected_ids).update(parent=0)
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:product_list')
        
        messages.warning(request, _("Product delete successfully!"))
        return redirect('isis:product_list')


def product_dashboard_view(request):
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    last_products =  Product.objects.all().order_by('-date_created')[:15]
    total_products =  Product.objects.all().count()
    all_products = Product.objects.all().order_by('name')
    
    context = {}
    context['total'] = total_products
    context['last'] = last_products
    context['all'] = all_products
    
    return render(request, 'isis/dashboardviews/product_dashboard.html', context=context)

@login_required
def product_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    product = get_object_or_404(Product, slug=slug)

    child_products = Product.objects.filter(parent=product.id)
    
    try:
        parent_product = Product.objects.get(id=product.parent)
    except Product.DoesNotExist:
        parent_product = _('No parent')

    context ={}
    # add the dictionary during initialization
    context["product"] = product    
    context["child_products"] = child_products    
    context["parent_product"] = parent_product    
    return render(request, "isis/detailviews/product_detail_view.html", context)


@login_required
def warehouse_create_view(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            warehouse = instance
            parent = request.POST.get('parent')
            
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent
            
            instance = instance.save()

            slug = slugify(warehouse.name)
            messages.success(request, _("Warehouse added successfully!"))

            if request.POST.get('save_warehouse'):
                return redirect('isis:warehouse_details', slug=slug)
            else:
                return redirect('isis:warehouse_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:warehouse_create')
    else:
        form = WarehouseForm()
        context = {'form': form}
        return render(request, 'isis/createviews/warehouse_create.html', context)


@login_required
def warehouse_list_view(request):
    warehouse = Warehouse.objects.all()
    context = {}
    context['object_list'] = warehouse

    return render(request, 'isis/listviews/warehouse_list.html', context) 


@login_required
def warehouse_update_view(request, slug):
    warehouse = get_object_or_404(Warehouse, slug=slug)
    form = WarehouseForm(request.POST or None, instance=warehouse)
	
    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()

            parent = request.POST.get('parent')
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent

                # Since parent returns the product id we need to get the name of the parent product
                parent_name =  get_model_name_from_id(Warehouse, parent)
                
                # If the updated product is same as parent
                if parent_name == warehouse.name:
                    print('Same product')
                    instance.parent = 0

            instance = instance.save()
            messages.success(request, _("Warehouse updated successfully!"))

            if request.POST.get('save_warehouse'):
                return redirect('isis:warehouse_list')
            else:
                return redirect('isis:warehouse_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:warehouse_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'isis/updateviews/warehouse_update.html', context)


@login_required
def warehouse_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Warehouse.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:warehouse_list')
        
        messages.warning(request, _("Warehouse delete successfully!"))
        return redirect('isis:warehouse_list')


@login_required
def warehouse_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    warehouse = get_object_or_404(Warehouse, slug=slug)

    child_warehouses = Warehouse.objects.filter(parent=warehouse.id)
    
    try:
        parent_warehouse = Warehouse.objects.get(id=warehouse.parent)
    except warehouse.DoesNotExist:
        parent_warehouse = _('No parent')

    context ={}
    # add the dictionary during initialization
    context["warehouse"] = warehouse    
    context["child_warehouses"] = child_warehouses    
    context["parent_warehouse"] = parent_warehouse 
    return render(request, "isis/detailviews/warehouse_detail_view.html", context)


@login_required
def tax_create_view(request):
    if request.method == 'POST':
        form = TaxForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            tax = instance
            instance = instance.save()
            
            slug = slugify(tax.name)
            
            messages.success(request, _("Tax added successfully!"))

            if request.POST.get('save_tax'):
                return redirect('isis:tax_list', slug=slug)
            else:
                return redirect('isis:tax_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:tax_create')
    else:
        form = TaxForm()
        context = {'form': form}
        return render(request, 'isis/createviews/tax_create.html', context)


@login_required
def tax_list_view(request):
    tax = Tax.objects.all()
    context = {}
    context['object_list'] = tax

    return render(request, 'isis/listviews/tax_list.html', context) 


@login_required
def tax_update_view(request, slug):
    tax = get_object_or_404(Tax, slug=slug)
    form = TaxForm(request.POST or None, instance=tax)
	
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Tax updated successfully!"))

            if request.POST.get('save_tax'):
                return redirect('isis:tax_list')
            else:
                return redirect('isis:tax_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:tax_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'isis/updateviews/tax_update.html', context)


@login_required
def tax_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Tax.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:tax_list')
        
        messages.warning(request, _("Tax delete successfully!"))
        return redirect('isis:tax_list')


@login_required
def tax_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    tax = get_object_or_404(Tax, slug=slug)

    context ={}
    # add the dictionary during initialization
    context["tax"] = tax    
    return render(request, "isis/detailviews/tax_detail_view.html", context)





