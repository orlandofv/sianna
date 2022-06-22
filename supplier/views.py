import datetime
import json
from decimal import Decimal
import sys
import os

from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
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
from django.contrib import messages #import messages
from django.utils.translation import ugettext_lazy as _
from config.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static

from config import utilities
from asset_app.models import Costumer

from .models import (SupplierInvoice, SupplierInvoiceItem)
from isis.models import (Costumer, Warehouse, Tax, Product)
from isis.forms import (PaymentTermForm, PaymentMethodForm)
from isis.views import increment_document_number, get_or_save_product, manage_stock
from users.models import User
from .forms import (SupplierInvoiceForm, SupplierInvoiceItemForm, SupplierForm)
from asset_app.models import (Costumer, Settings)
from warehouse.forms import WarehouseForm

########################## Costumer ##########################
class SupplierListView(LoginRequiredMixin, ListView):
    queryset = Costumer.objects.filter(is_supplier=1)
    template_name = 'asset_app/listviews/costumer_list_view.html'


@login_required
def supplier_create_view(request):
    if request.method == 'POST':

        form = SupplierForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            
            parent = request.POST.get('parent')
            
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent

            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Costumer added successfully!"))

            if request.POST.get('save_costumer'):
                return redirect('asset_app:supplier_list')
            else:
                return redirect('asset_app:supplier_create')
        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:supplier_create')
    else:
        form = SupplierForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/costumer_create.html', context)


@login_required
def supplier_update_view(request, slug):
    costumer = get_object_or_404(Costumer, slug=slug)
    form = SupplierForm(request.POST or None, instance=costumer)

    if request.method == 'POST':
        
        if form.is_valid():
            print(request.POST)
            
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()

            parent = request.POST.get('parent')
            if parent == "":
                instance.parent = 0
            else:
                instance.parent = parent

            instance = instance.save()
            messages.success(request, _("Costumer updated successfully!"))

            if request.POST.get('save_costumer'):
                return redirect('asset_app:supplier_list')
            else:
                return redirect('asset_app:supplier_create')

        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:supplier_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/costumer_update.html', context)


@login_required
def supplier_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Costumer.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('asset_app:supplier_list')
        
        messages.warning(request, _("Costumer delete successfully!"))
        return redirect('asset_app:supplier_list')


@login_required
def supplier_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    costumer = get_object_or_404(Costumer, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = costumer    
    return render(request, "asset_app/detailviews/costumer_detail_view.html", context)


@login_required
def invoice_list_view(request):
    invoice = SupplierInvoice.objects.all()
    context = {}
    context['object_list'] = invoice

    return render(request, 'supplier/listviews/invoice_list.html', context) 


@login_required
def invoice_create_view(request):
    if request.method == 'POST':
        form = SupplierInvoiceForm(request.POST)
        costumer_form = SupplierForm(request.POST)
        warehouse_form = WarehouseForm(request.POST)
        payment_term_form = PaymentTermForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST)

        if form.is_valid() or costumer_form.is_valid() or warehouse_form.is_valid() \
            or payment_method_form.is_valid() or payment_term_form.is_valid():
            if request.POST.get('save_costumer') or request.POST.get('save_costumer_new'):
                instance = costumer_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            if request.POST.get('save_payment_method') or request.POST.get('save_payment_method_new'):
                instance = payment_method_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            if request.POST.get('save_payment_term') or request.POST.get('save_payment_method_term'):
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            
            document_number = increment_document_number(SupplierInvoice)

            instance.number = document_number
            name = '{} {}'.format(_('Invoice'), document_number)
            instance.name = name
            instance.slug = slugify(name)
            
            invoice = instance
            instance = instance.save()
            
            slug = slugify(invoice.name)

            messages.success(request, _("SupplierInvoice added successfully!"))

            return redirect('supplier:invoice_item_create', slug=slug)

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('supplier:invoice_create')
    else:
        form = SupplierInvoiceForm()
        costumer_form = SupplierForm()
        warehouse_form = WarehouseForm()
        payment_term_form = PaymentTermForm()
        payment_method_form = PaymentMethodForm()

        context = {'form': form, 'costumer_form': costumer_form, 
        'warehouse_form': warehouse_form, 'payment_term_form': payment_term_form,
        'payment_method_form': payment_method_form}
        return render(request, 'supplier/createviews/invoice_create.html', context)


def get_model_name_from_id(model, id):
    try:
        invoice = model.objects.get(id=id)
        return invoice.name
    except SupplierInvoice.DoesNotExist:
        return None


@login_required
def invoice_update_view(request, slug):
    invoice = get_object_or_404(SupplierInvoice, slug=slug)
    invoice_number = invoice.number
    form = SupplierInvoiceForm(request.POST or None, instance=invoice)
    costumer_form = SupplierForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)
    payment_term_form = PaymentTermForm(request.POST or None)
    payment_method_form = PaymentMethodForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid() or costumer_form.is_valid() or warehouse_form.is_valid():
            if request.POST.get('save_costumer') or request.POST.get('save_costumer_new'):
                instance = costumer_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')

            if request.POST.get('save_payment_method') or request.POST.get('save_payment_method_new'):
                instance = payment_method_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            if request.POST.get('save_payment_term') or request.POST.get('save_payment_method_term'):
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('supplier:invoice_create')
            
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance.number = invoice_number
            instance = instance.save()
            messages.success(request, _("SupplierInvoice updated successfully!"))

            if request.POST.get('save_invoice'):
                return redirect('supplier:invoice_details', slug=slug)
            else:
                return redirect('supplier:invoice_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('supplier:invoice_update', slug=slug)

    context = {'form': form, 'costumer_form': costumer_form, 'warehouse_form': warehouse_form, 
    'payment_term_form': payment_term_form,'payment_method_form': payment_method_form}

    return render(request, 'supplier/updateviews/invoice_update.html', context)


@login_required
def invoice_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    SupplierInvoice.objects.filter(id__in=selected_ids).delete()
                    # Set parent to No parent in invoices with deleted parents
                    SupplierInvoice.objects.filter(parent__in=selected_ids).update(parent=0)
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('supplier:invoice_list')
        
        messages.warning(request, _("SupplierInvoice delete successfully!"))
        return redirect('supplier:invoice_list')


def invoice_dashboard_view(request):
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    last_invoices =  SupplierInvoice.objects.all().order_by('-date_created')[:15]
    total_invoices =  SupplierInvoice.objects.all().count()
    all_invoices = SupplierInvoice.objects.all().order_by('name')
    
    context = {}
    context['total'] = total_invoices
    context['last'] = last_invoices
    context['all'] = all_invoices
    
    return render(request, 'supplier/dashboardviews/invoice_dashboard.html', context=context)

@login_required
def invoice_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    invoice = get_object_or_404(SupplierInvoice, slug=slug)

    paid_invoices = SupplierInvoice.objects.filter(supplier=invoice.supplier, 
    paid_status=1).exclude(id=invoice.id).order_by('-number')[:5]
    
    overdue_invoices = SupplierInvoice.objects.filter(supplier=invoice.supplier, 
    paid_status=0, due_date__lt=datetime.datetime.now()).exclude(id=invoice.id).order_by('number')
    
    not_paid_invoices = SupplierInvoice.objects.filter(supplier=invoice.supplier, 
    paid_status=0).exclude(id=invoice.id).order_by('number')
    
    context ={}
    # add the dictionary during initialization
    context["invoice"] = invoice    
    context["paid_invoices"] = paid_invoices     
    context["not_paid_invoices"] = not_paid_invoices     
    context["overdue_invoices"] = overdue_invoices     
    return render(request, "supplier/detailviews/invoice_detail_view.html", context)


@login_required
def invoice_item_create_view(request, slug):

    invoice = get_object_or_404(SupplierInvoice, slug=slug)
    items = SupplierInvoiceItem.objects.filter(invoice=invoice)

    tax_total = items.aggregate(Sum('tax_total'))
    discount_total = items.aggregate(Sum('discount_total'))
    sub_total = items.aggregate(Sum('sub_total'))
    total = items.aggregate(Sum('total'))

    if request.method == 'POST':
        form = SupplierInvoiceItemForm(request.POST)

        if request.POST.get('validate'):
            document = '{} - {}'.format(_('Invoice'), invoice.id) 
            if invoice.finished_status == 0:
                for i in items:
                    manage_stock(request, document ,i.product, i.quantity, invoice.warehouse, invoice.supplier,
                    "Supplier Invoice" 
                )

            i = SupplierInvoice.objects.filter(slug=slug).update(finished_status=1)
            return redirect('supplier:invoice_list')         
        else:
            name = request.POST.get('product')
            quantity = Decimal(request.POST.get('quantity'))
            tax = Decimal(request.POST.get('tax'))
            discount = Decimal(request.POST.get('discount'))
            price = Decimal(request.POST.get('price'))
            warehouse = invoice.warehouse

            # Gets or saves the product information
            product_object = get_or_save_product(request, name, tax, warehouse)
            print(product_object)

            # save the data and after fetch the object in instance
            instance = SupplierInvoiceItem(invoice=invoice, tax=tax, quantity=quantity,
            discount= discount, price=price, product=product_object) 
            instance.save()

        return redirect('supplier:invoice_item_create', slug=slug)
    else:
        form = SupplierInvoiceItemForm(None)
        return render(request, 'supplier/createviews/invoice_item_create.html', 
        {'invoice': invoice, 'form': form, 'items': items, 'tax_total': tax_total, 
        'discount_total': discount_total, 'sub_total': sub_total, 'total': total})


@login_required
def invoice_item_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        print(selected_ids)

        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    SupplierInvoiceItem.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}.".format(e)))
                    return redirect('supplier:invoice_create')

        return redirect('supplier:invoice_create')

