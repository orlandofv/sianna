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
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static

from config import utilities
from asset_app.forms import CostumerForm
from asset_app.models import Costumer
from .models import (Gallery, Product, Tax, Warehouse, Invoice, PaymentTerm, PaymentMethod, Receipt, 
InvoiceItem, StockMovement)
from users.models import User
from .forms import (ProductForm, TaxForm, PaymentTermForm, 
PaymentMethodForm, ReceiptForm, InvoiceItemForm)

from warehouse.models import Warehouse
from warehouse.forms import WarehouseForm
from asset_app.models import (Costumer, Settings)


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
    except model.DoesNotExist:
        return None

@login_required
def product_update_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=product)
    tax_form = TaxForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)

    if request.method == 'POST':

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


@login_required
def invoice_list_view(request):
    invoice = Invoice.objects.all()
    context = {}
    context['object_list'] = invoice

    return render(request, 'isis/listviews/invoice_list.html', context) 

def increment_document_number(model):
    # Returns the first object matched by the queryset, or None if there is no matching object. 
    i = model.objects.order_by('-id').first()
    if i is not None:
        document_number = i.number + 1
    else:
        document_number = 1

    return document_number

@login_required
def invoice_create_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        costumer_form = CostumerForm(request.POST)
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

                return redirect('isis:invoice_create')
            
            if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')
            
            if request.POST.get('save_payment_method') or request.POST.get('save_payment_method_new'):
                instance = payment_method_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')
            
            if request.POST.get('save_payment_term') or request.POST.get('save_payment_method_term'):
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')
            
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            
            document_number = increment_document_number(Invoice)

            instance.number = document_number
            name = '{} {}'.format(_('Invoice'), document_number)
            instance.name = name
            instance.slug = slugify(name)
            
            invoice = instance
            instance = instance.save()
            
            slug = slugify(invoice.name)

            messages.success(request, _("Invoice added successfully!"))

            return redirect('isis:invoice_item_create', slug=slug)

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:invoice_create')
    else:
        form = InvoiceForm()
        costumer_form = CostumerForm()
        warehouse_form = WarehouseForm()
        payment_term_form = PaymentTermForm()
        payment_method_form = PaymentMethodForm()

        context = {'form': form, 'costumer_form': costumer_form, 
        'warehouse_form': warehouse_form, 'payment_term_form': payment_term_form,
        'payment_method_form': payment_method_form}
        return render(request, 'isis/createviews/invoice_create.html', context)


@login_required
def invoice_update_view(request, slug):
    invoice = get_object_or_404(Invoice, slug=slug)
    form = InvoiceForm(request.POST or None, instance=invoice)
    costumer_form = CostumerForm(request.POST or None)
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

                return redirect('isis:invoice_create')
            
            if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')

            if request.POST.get('save_payment_method') or request.POST.get('save_payment_method_new'):
                instance = payment_method_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')
            
            if request.POST.get('save_payment_term') or request.POST.get('save_payment_method_term'):
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoice_create')
            
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Invoice updated successfully!"))

            if request.POST.get('save_invoice'):
                return redirect('isis:invoice_details', slug=slug)
            else:
                return redirect('isis:invoice_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:invoice_update', slug=slug)

    context = {'form': form, 'costumer_form': costumer_form, 'warehouse_form': warehouse_form,}
    return render(request, 'isis/updateviews/invoice_update.html', context)


@login_required
def invoice_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Invoice.objects.filter(id__in=selected_ids).delete()
                    # Set parent to No parent in invoices with deleted parents
                    Invoice.objects.filter(parent__in=selected_ids).update(parent=0)
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:invoice_list')
        
        messages.warning(request, _("Invoice delete successfully!"))
        return redirect('isis:invoice_list')


def invoice_dashboard_view(request):
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    last_invoices =  Invoice.objects.all().order_by('-date_created')[:15]
    total_invoices =  Invoice.objects.all().count()
    all_invoices = Invoice.objects.all().order_by('name')
    
    context = {}
    context['total'] = total_invoices
    context['last'] = last_invoices
    context['all'] = all_invoices
    
    return render(request, 'isis/dashboardviews/invoice_dashboard.html', context=context)

@login_required
def invoice_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    invoice = get_object_or_404(Invoice, slug=slug)

    paid_invoices = Invoice.objects.filter(costumer=invoice.costumer, 
    paid_status=1).exclude(id=invoice.id).order_by('-number')[:5]
    
    overdue_invoices = Invoice.objects.filter(costumer=invoice.costumer, 
    paid_status=0, due_date__lt=datetime.datetime.now()).exclude(id=invoice.id).order_by('number')
    
    not_paid_invoices = Invoice.objects.filter(costumer=invoice.costumer, 
    paid_status=0).exclude(id=invoice.id).order_by('number')
    
    context ={}
    # add the dictionary during initialization
    context["invoice"] = invoice    
    context["paid_invoices"] = paid_invoices     
    context["not_paid_invoices"] = not_paid_invoices     
    context["overdue_invoices"] = overdue_invoices     
    return render(request, "isis/detailviews/invoice_detail_view.html", context)


def get_or_save_product(request, product_name, tax, warehouse):
    print(product_name)
    try:
        product = Product.objects.get(name=product_name)
    except Product.DoesNotExist:
        product = None

    if not product:
        import random

        user = request.user
        chars = 'ABCDEFGHIJKLMNOPKRSTUVXYZabcdefghijklmnopkqrstuvxwz1234567890'
        code = ''.join(random.choice(chars) for i in range(8))
        type = request.POST.get('type')
        tax_object = Tax.objects.get(rate=tax)

        slug = slugify(product_name)
        product = Product(code=code, name=product_name, slug=slug, tax=tax_object, warehouse=warehouse, 
        created_by=user, modified_by=request.user, type=type)
        product.save()
    
    return product

def get_static(path):
    if settings.DEBUG:
        return find(path)
    else:
        return static(path)

def create_pdf():
    from PyQt5 import QtWidgets, QtWebEngineWidgets
    from PyQt5.QtCore import QUrl
    from PyQt5.QtGui import QPageLayout, QPageSize
    from PyQt5.QtWidgets import QApplication
    from django.templatetags.static import static

    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    layout = QPageLayout()
    layout.setPageSize(QPageSize(QPageSize.A5))
    layout.setOrientation(QPageLayout.Portrait)
    file = get_static('documents/invoice.html')
    file_path = str(os.path.realpath(file)).replace('\\', '/')
    print(file_path)
    print(settings.STATIC_URL)
    loader.load(QUrl('file:///{}'.format(file_path)))

    loader.page().pdfPrintingFinished.connect(lambda *args: QApplication.exit())

    def emit_pdf(finished):
        loader.page().printToPdf("test.pdf", pageLayout=layout)

    loader.loadFinished.connect(emit_pdf)
    sys.exit(app.exec_())

def manage_stock(request,  document, product, quantity, warehouse):
    user = request.user
    date = datetime.datetime.now()

    stock = StockMovement(product=product, document=document, quantity=quantity, warehouse=warehouse,
    modified_by=user, created_by=user, date_modified=date, date_created=date)
    stock.save()

    return stock

@login_required
def invoice_show(request, slug):
    invoice = get_object_or_404(Invoice, slug=slug)
    items = InvoiceItem.objects.filter(invoice=invoice)

    tax_total = items.aggregate(Sum('tax_total'))
    discount_total = items.aggregate(Sum('discount_total'))
    sub_total = items.aggregate(Sum('sub_total'))
    total = items.aggregate(Sum('total'))

    costumer = Costumer.objects.get(id=invoice.costumer.id)
    company = Settings.objects.first()

    context = {'invoice': invoice, 'items': items, 'tax_total': tax_total, 
    'discount_total': discount_total, 'sub_total': sub_total, 
    'total': total, 'costumer': costumer, 'company': company}

    instance = Invoice.objects.filter(id=invoice.id).update(finished_status=1)
    messages.success(request, _("Add some algo!"))
    return render(request, 'isis/documents/invoice.html', context) 


@login_required
def invoice_item_create_view(request, slug):

    invoice = get_object_or_404(Invoice, slug=slug)
    items = InvoiceItem.objects.filter(invoice=invoice)

    tax_total = items.aggregate(Sum('tax_total'))
    discount_total = items.aggregate(Sum('discount_total'))
    sub_total = items.aggregate(Sum('sub_total'))
    total = items.aggregate(Sum('total'))

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)

        if request.POST.get('validate'):
            document = '{} - {}'.format(_('Invoice'), invoice.id) 
            if invoice.finished_status == 0:
                for i in items:
                    manage_stock(request, document ,i.product, -i.quantity, invoice.warehouse 
                )
            
            invoice_show(request, slug)
            return redirect('isis:invoice_show', slug=slug)         
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
            instance = InvoiceItem(invoice=invoice, tax=tax, quantity=quantity,
            discount= discount, price=price, product=product_object) 
            instance.save()

            
        return redirect('isis:invoice_item_create', slug=slug)
    else:
        form = InvoiceItemForm(None)
        return render(request, 'isis/createviews/invoice_item_create.html', 
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
                    InvoiceItem.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}.".format(e)))
                    return redirect('isis:invoice_create')

        return redirect('isis:invoice_create')


@login_required
def payment_method_create_view(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            payment_method = instance
            instance = instance.save()

            slug = slugify(payment_method.name)
            messages.success(request, _("PaymentMethod added successfully!"))

            if request.POST.get('save_payment_method'):
                return redirect('isis:payment_method_details', slug=slug)
            else:
                return redirect('isis:payment_method_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:payment_method_create')
    else:
        form = PaymentMethodForm()
        context = {'form': form}
        return render(request, 'isis/createviews/payment_method_create.html', context)


@login_required
def payment_method_list_view(request):
    payment_method = PaymentMethod.objects.all()
    context = {}
    context['object_list'] = payment_method

    return render(request, 'isis/listviews/payment_method_list.html', context) 


@login_required
def payment_method_update_view(request, slug):
    payment_method = get_object_or_404(PaymentMethod, slug=slug)
    form = PaymentMethodForm(request.POST or None, instance=payment_method)
	
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("PaymentMethod updated successfully!"))

            if request.POST.get('save_payment_method'):
                return redirect('isis:payment_method_list')
            else:
                return redirect('isis:payment_method_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:payment_method_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'isis/updateviews/payment_method_update.html', context)


@login_required
def payment_method_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    PaymentMethod.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:payment_method_list')
        
        messages.warning(request, _("PaymentMethod delete successfully!"))
        return redirect('isis:payment_method_list')


@login_required
def payment_term_create_view(request):
    if request.method == 'POST':
        form = PaymentTermForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            payment_term = instance
            instance = instance.save()

            slug = slugify(payment_term.name)
            messages.success(request, _("PaymentTerm added successfully!"))

            if request.POST.get('save_payment_term'):
                return redirect('isis:payment_term_details', slug=slug)
            else:
                return redirect('isis:payment_term_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:payment_term_create')
    else:
        form = PaymentTermForm()
        context = {'form': form}
        return render(request, 'isis/createviews/payment_term_create.html', context)


@login_required
def payment_term_list_view(request):
    payment_term = PaymentTerm.objects.all()
    context = {}
    context['object_list'] = payment_term

    return render(request, 'isis/listviews/payment_term_list.html', context) 


@login_required
def payment_term_update_view(request, slug):
    payment_term = get_object_or_404(PaymentTerm, slug=slug)
    form = PaymentTermForm(request.POST or None, instance=payment_term)
	
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("PaymentTerm updated successfully!"))

            if request.POST.get('save_payment_term'):
                return redirect('isis:payment_term_list')
            else:
                return redirect('isis:payment_term_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:payment_term_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'isis/updateviews/payment_term_update.html', context)


@login_required
def payment_term_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    PaymentTerm.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:payment_term_list')
        
        messages.warning(request, _("PaymentTerm delete successfully!"))
        return redirect('isis:payment_term_list')


@login_required
def receipt_create_view(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            receipt = instance
            instance = instance.save()

            slug = slugify(receipt.name)
            messages.success(request, _("Receipt added successfully!"))

            if request.POST.get('save_receipt'):
                return redirect('isis:receipt_details', slug=slug)
            else:
                return redirect('isis:receipt_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:receipt_create')
    else:
        form = ReceiptForm()
        context = {'form': form}
        return render(request, 'isis/createviews/receipt_create.html', context)


@login_required
def receipt_list_view(request):
    receipt = Receipt.objects.all()
    context = {}
    context['object_list'] = receipt

    return render(request, 'isis/listviews/receipt_list.html', context) 


@login_required
def receipt_update_view(request, slug):
    receipt = get_object_or_404(Receipt, slug=slug)
    form = ReceiptForm(request.POST or None, instance=receipt)
	
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Receipt updated successfully!"))

            if request.POST.get('save_receipt'):
                return redirect('isis:receipt_list')
            else:
                return redirect('isis:receipt_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:receipt_update', slug=slug)
    
    context = {'form': form}
    return render(request, 'isis/updateviews/receipt_update.html', context)


@login_required
def receipt_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Receipt.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:receipt_list')
        
        messages.warning(request, _("Receipt delete successfully!"))
        return redirect('isis:receipt_list')

