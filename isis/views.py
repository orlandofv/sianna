import datetime
import json
from decimal import Decimal
import sys
import os

from django.db.models import DecimalField
from django.db.models import Sum, Value as V, F, Q
from django.db.models.functions import Coalesce
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
from django.forms import ValidationError

from config import utilities
from asset_app.forms import CostumerForm
from asset_app.models import Costumer
from .models import (Gallery, Product, Tax, Warehouse, Invoice, PaymentTerm, PaymentMethod, Receipt, 
InvoiceItem, Category, ReceiptInvoice, Document, Invoicing, InvoicingItem, DocumentPayment)
from users.models import User
from .forms import (ProductForm, TaxForm, PaymentTermForm, 
PaymentMethodForm, ReceiptForm, InvoiceItemForm, InvoiceForm, CategoryForm, 
DocumentForm, InvoicingForm, InvoicingItemForm)

from warehouse.models import Warehouse
from warehouse.forms import WarehouseForm
from asset_app.models import (Costumer, Settings)
from stock.models import Stock
from stock.forms import StockSearchForm

from utilities import increment_invoice_number, increment_document_number

PRODUCT_SAVED = False


########################## Category ##########################
class CategoryListView(LoginRequiredMixin, ListView):
    queryset = Category.objects.all()
    template_name = 'isis/listviews/category_list.html'


@login_required
def category_create_view(request):
    if request.method == 'POST':

        form = CategoryForm(request.POST, request.FILES)
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
            messages.success(request, _("Category added successfully!"))

            if request.POST.get('save_category'):
                return redirect('isis:category_list')
            else:
                return redirect('isis:category_create')
        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:category_create')
    else:
        form = CategoryForm()
        context = {'form': form}
        return render(request, 'isis/createviews/category_create.html', context)


@login_required
def category_update_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

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
            messages.success(request, _("Category updated successfully!"))

            if request.POST.get('save_category'):
                return redirect('isis:category_list')
            else:
                return redirect('isis:category_create')

        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:category_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'isis/updateviews/category_update.html', context)


@login_required
def category_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Category.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:category_list')
        
        messages.warning(request, _("Category delete successfully!"))
        return redirect('isis:category_list')


@login_required
def category_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    category = get_object_or_404(Category, slug=slug)

    child_categories = Category.objects.filter(parent=category.id)
    
    try:
        parent_category = Category.objects.get(id=category.parent)
    except Category.DoesNotExist:
        parent_category = _('No parent')

    context ={}
    # add the dictionary during initialization
    context["category"] = category    
    context["child_categories"] = child_categories    
    context["parent_category"] = parent_category
   
    return render(request, "isis/detailviews/category_detail_view.html", context)


@login_required
def product_list_view(request):
    product = Product.objects.all()
    context = {}
    context['object_list'] = product

    return render(request, 'isis/listviews/product_list.html', context) 

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        tax_form = TaxForm(request.POST)
        warehouse_form = WarehouseForm(request.POST)
        category_form = CategoryForm(request.POST)
        
        if form.is_valid() or tax_form.is_valid() or warehouse_form.is_valid() \
        or category_form.is_valid:
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
            
            if request.POST.get('save_category') or request.POST.get('save_category_new'):
                instance = category_form.save(commit=False)
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
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:product_create')
    else:
        form = ProductForm()
        tax_form = TaxForm()
        warehouse_form = WarehouseForm()
        category_form = CategoryForm()
        
        context = {'form': form, 'tax_form': tax_form, 
        'warehouse_form': warehouse_form, 'category_form': category_form}

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
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    tax_form = TaxForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)
    category_form = CategoryForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid() or tax_form.is_valid() or warehouse_form.is_valid() \
        or category_form.is_valid:
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

            if request.POST.get('save_category') or request.POST.get('save_category_new'):
                instance = category_form.save(commit=False)
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

    context = {'form': form, 'tax_form': tax_form, 'warehouse_form': warehouse_form,
    'category_form': category_form,}
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

def get_product_type(product):
    if product.type == "PRODUCT":
        return 'Product'
    return 'Service'

@login_required
def product_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    product = get_object_or_404(Product, slug=slug)

    product_type = get_product_type(product)
    
    context ={}
    # add the dictionary during initialization
    context["product"] = product     
    context["product_type"] = product_type    

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

    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    if request.method == "POST":
        search_form = StockSearchForm(request.POST)
        start_date = request.POST.get("start_date".replace('T', " "))
        end_date = request.POST.get("end_date")

        invoice = Invoice.objects.raw("""
        SELECT inv.*, SUM(item.discount_total) AS ds, SUM(item.sub_total) AS sb, 
        SUM(item.tax_total) AS tax, SUM(item.total) AS tt 
        FROM isis_invoice AS inv
        LEFT JOIN isis_invoiceitem item ON inv.id=item.invoice_id
        WHERE inv.date_created BETWEEN '{}' AND '{}'
        GROUP BY inv.id  
        """.format(str(start_date).replace('T', " "), str(end_date).replace('T', " ")))
    else:
        search_form = StockSearchForm()
        invoice = Invoice.objects.raw("""
        SELECT inv.*, SUM(item.discount_total) AS ds, SUM(item.sub_total) AS sb, 
        SUM(item.tax_total) AS tax, SUM(item.total) AS tt 
        FROM isis_invoice AS inv
        LEFT JOIN isis_invoiceitem item ON inv.id=item.invoice_id
        WHERE inv.date_created BETWEEN '{}' AND '{}'
        GROUP BY inv.id  """.format(start_date, end_date))
    
    context = {}
    context['search_form'] = search_form
    context['object_list'] = invoice

    return render(request, 'isis/listviews/invoice_list.html', context) 

def get_product_name(id):
    try:
        product = Product.objects.get(id=id)
        return product
    except Product.DoesNotExist:
        return None


def get_product_id(product_name):
    try:
        product = Product.objects.get(name=product_name)
        return product
    except Product.DoesNotExist:
        return None


def get_or_save_product(request, product_id, tax, warehouse):

    print(product_id)
    # Session that controls if the product was added dinamically or not 
    # Sessions work as global variables
    new_product = request.session.get('new_product')

    print('New product ', new_product)
    try:
        # Workaround to avoid product duplication error on DB
        if new_product:
            product = Product.objects.filter(name=product_id).first()
            request.session['new_product'] = False
        else:
            product = Product.objects.filter(id=int(product_id)).first()
    except (Product.DoesNotExist, ValueError) as e:
        print(e)
        product = None
    
    print(product)

    if not product:
        print('No product')
        if request.user.is_staff:
            import random

            user = request.user
            chars = 'ABCDEFGHIJKLMNOPKRSTUVXYZabcdefghijklmnopkqrstuvxwz1234567890'
            code = ''.join(random.choice(chars) for i in range(8))
            type = request.POST.get('type') or 'PRODUCT'
            sell_price = request.POST.get('price') or '0'
            tax_object = Tax.objects.get(rate=tax) or '0'

            category = Category.objects.all().first()

            slug = slugify(product_id)
            product = Product(code=code, name=product_id, slug=slug, tax=tax_object, warehouse=warehouse, 
            created_by=user, category=category, modified_by=request.user, type=type, sell_price=sell_price)
            product.save()

            print('Product saved ', product)
            # Session that controls if the product was added dinamically or not 
            request.session['new_product'] = True

        else:
            messages.error(request, _("Please contact Administrator to add new Products!"))
        
    return product


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
    
            document_number = increment_invoice_number(Invoice)

            instance.number = document_number
            name = '{} {}'.format(_('Invoice'), document_number)
            instance.name = name
            slug = slugify(name)
            instance.slug = slug
            instance = instance.save()

            messages.success(request, _("Invoice created successfully!"))

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

    if invoice.is_finished():
        messages.warning(request,_('Invoice is closed and cannot be edited.'))
        return redirect('isis:invoice_list')

    form = InvoiceForm(request.POST or None, instance=invoice)
    costumer_form = CostumerForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)
    payment_term_form = PaymentTermForm(request.POST or None)
    payment_method_form = PaymentMethodForm(request.POST or None)

    invoice_number = invoice.number

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
            instance.number = invoice_number
            instance = instance.save()
            messages.success(request, _("Invoice updated successfully!"))
            
            return redirect('isis:invoice_item_create', slug=slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:invoice_update', slug=slug)

    context = {'form': form, 'costumer_form': costumer_form, 
        'warehouse_form': warehouse_form, 'payment_term_form': payment_term_form,
        'payment_method_form': payment_method_form}
    return render(request, 'isis/createviews/invoice_create.html', context)


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
    payments = ReceiptInvoice.objects.filter(invoice=invoice)

    total_payment = [Invoice.objects.filter(id=i.invoice_id) for i in payments]

    total = total_payment[0].aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))
    total_paid = payments.aggregate(total=Coalesce(Sum('paid'), V(0), output_field=DecimalField()))
    total_debt = payments.aggregate(total=Coalesce(Sum('remaining'), V(0), output_field=DecimalField()))

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
    context["payments"] = payments
    context["total"] = total
    context["total_paid"] = total_paid
    context["total_debt"] = total_debt
    
    return render(request, "isis/detailviews/invoice_detail_view.html", context)


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
    app.exec_()

def manage_stock(request,  document, product, quantity, warehouse, costumer, origin):
    user = request.user
    date = datetime.datetime.now()

    stock = Stock(product=product, document=document, quantity=quantity, warehouse=warehouse,
    costumer=costumer, origin=origin, modified_by=user, created_by=user, date_modified=date, date_created=date)
    stock.save()

    return stock

def load_sell_prices(request):
    print(request.POST)
    print(request.GET)
    product_id = request.GET.get('product')
    
    warehouse = Warehouse.objects.all().first()
    tax = Tax.objects.all().first()

    product_object = get_or_save_product(request, product_id, tax.rate, warehouse)
    
    try:
        prices = Product.objects.get(id=product_object.id)
        return render(request, 'isis/partials/sell_price_list.html', {'prices': prices})
    except Product.DoesNotExist as e:
        print(e)
    
    
@login_required
def invoice_show(request, slug):
    """
    Displays Invoice for printing, export, ...
    """
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
    return render(request, 'isis/documents/invoice.html', context) 


@login_required
def receipt_show(request, slug):
    """
    Displays Receipt for printing, export, ...
    """
    receipt = get_object_or_404(Receipt, slug=slug)
    items = ReceiptInvoice.objects.filter(receipt=receipt)


    total = items.aggregate(total=Coalesce(Sum('paid'), V(0), output_field=DecimalField()))

    costumer = Costumer.objects.get(id=receipt.costumer.id)
    company = Settings.objects.first()

    context = {'receipt': receipt, 'items': items,  
    'total': total, 'costumer': costumer, 'company': company}

    return render(request, 'documents/receipt.html', context) 

@login_required
def invoice_item_create_view(request, slug):
    """
    Creates or Adds Invoice Items
    """
    invoice = get_object_or_404(Invoice, slug=slug)
    
    if invoice.is_finished():
        messages.warning(request,_('Invoice is closed and cannot be edited.'))
        return redirect('isis:invoice_list')

    items = InvoiceItem.objects.filter(invoice=invoice)

    tax_total = items.aggregate(tax=Coalesce(Sum('tax_total'), V(0), output_field=DecimalField()))
    discount_total = items.aggregate(discount=Coalesce(Sum('discount_total'), V(0), output_field=DecimalField()))
    sub_total = items.aggregate(subtotal=Coalesce(Sum('sub_total'), V(0), output_field=DecimalField()))
    total = items.aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)

        if request.POST.get('validate'):
            document = '{} - {}'.format(_('Invoice'), invoice.id)

            # Records stock movement 
            if invoice.finished_status == 0:
                for i in items:
                    manage_stock(request, document, i.product, -i.quantity, invoice.warehouse, invoice.costumer, 
                "Costumer Invoice")
            
            # Changes the Invoice status to finished_status
            inv = Invoice.objects.filter(id=invoice.id).update(finished_status=1)
            invoice_show(request, slug)
            return redirect('isis:invoice_show', slug=slug)         
        else:
            # Records a line to Invoice
            name = request.POST.get('product')
            quantity = Decimal(request.POST.get('quantity'))
            tax = Decimal(request.POST.get('tax'))
            discount = Decimal(request.POST.get('discount'))
            price = Decimal(request.POST.get('price'))
            warehouse = invoice.warehouse

            # Gets or saves the product information
            product_object = get_or_save_product(request, name, tax, warehouse)
            print(product_object)

            if not product_object:
                return redirect('isis:invoice_item_create', slug=slug)

            # save the data and after fetch the object in instance
            instance = InvoiceItem(invoice=invoice, tax=tax, quantity=quantity,
            discount= discount, price=price, product=product_object) 
            instance.save()
            
            increase_decrease_invoice_totals(invoice.id)

        return redirect('isis:invoice_item_create', slug=slug)
    else:
        form = InvoiceItemForm(None)
        return render(request, 'isis/createviews/invoice_item_create.html', 
        {'invoice': invoice, 'form': form, 'items': items, 'tax_total': tax_total, 
        'discount_total': discount_total, 'sub_total': sub_total, 'total': total})


def increase_decrease_invoice_totals(invoice_id):
    """
    Modifies (Decreases or increases) Invoice totals when item is deleted
    """

    items = InvoiceItem.objects.filter(invoice=invoice_id)

    tax_total = items.aggregate(tax=Coalesce(Sum('tax_total'), V(0), output_field=DecimalField()))
    discount_total = items.aggregate(discount=Coalesce(Sum('discount_total'), V(0), output_field=DecimalField()))
    sub_total = items.aggregate(subtotal=Coalesce(Sum('sub_total'), V(0), output_field=DecimalField()))
    total = items.aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))

    inv = Invoice.objects.filter(id=invoice_id).update(
    debit=total['total'],
    total=total['total'],
    subtotal=sub_total['subtotal'],
    total_tax=tax_total['tax'],
    total_discount=discount_total['discount']
    )

    return inv


def get_invoice_from_items(item_id):
    try:
        Invoice.objects.get()
    except Exception:
        print('Not possible')


@login_required
def invoice_item_delete_view(request):
    
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        
        print(selected_ids)
        if len(selected_ids) == 1 and selected_ids[0] == 'None':
            return redirect('isis:invoice_item_create')

        if len(selected_ids) > 1:
            item = InvoiceItem.objects.filter(id=int(selected_ids[1])).first()
        else:
            item = InvoiceItem.objects.filter(id=int(selected_ids[0])).first()

        try:
            InvoiceItem.objects.filter(id__in=selected_ids).delete()
            increase_decrease_invoice_totals(item.invoice_id)
        except Exception as e:
            messages.warning(request, _("Not Deleted! {}.".format(e)))
            print(e)
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


class ReceiptListView(LoginRequiredMixin, ListView):
    model = Receipt
    template_name = 'isis/listviews/receipt_list.html'

def make_payment(receipt, invoice, debit, credit, total, payment):
    print(receipt, debit, invoice, credit, total, payment)
    
    # Total payment is equal or superior to debt
    if Decimal(payment) + Decimal(credit) >= Decimal(total):
        payment = Decimal(total) - Decimal(credit)
        inv = Invoice.objects.filter(id=invoice.id).update(
            credit=Decimal(total),
            debit=0,
            paid_status=1
            )
    else:
        inv = Invoice.objects.filter(id=invoice.id).update(
            credit=F('credit') + Decimal(payment),
            debit=F('debit') - Decimal(payment)
        )

    r = ReceiptInvoice(receipt=receipt, invoice=invoice, debit=Decimal(debit),
    paid=Decimal(payment), remaining=invoice.debit-Decimal(payment))
    r.save()

    return inv


@login_required
def receipt_invoice_view(request, slug):
    receipt = get_object_or_404(Receipt, slug=slug)

    if receipt.is_finished():
        messages.warning(request,_('Receipt is closed and cannot be edited.'))
        return redirect('isis:receipt_list')

    invoices = Invoice.objects.filter(costumer=receipt.costumer,
    paid_status=0, active_status=1, finished_status=1).order_by('date_created')

    if not invoices:
        messages.warning(request, _("This costumer has no pending invoices!"))
        return redirect('isis:receipt_list')

    if request.method == 'POST':
        # convert django query dict to python dictionary
        data = dict(request.POST)
        invoices = data['invoices']
        t = 0
        for inv in invoices:
            credit = data['invoice_credit'][t]
            total = data['invoice_total'][t]
            payment = data['payment'][t]
            debit = data['invoice_debit'][t]

            print(credit, total, payment)

            invoice = Invoice.objects.get(id=int(inv))

            make_payment(receipt, invoice, debit, credit, total, payment)
            t += 1

        Receipt.objects.filter(id=receipt.id).update(finished_status=1)
        return redirect('isis:receipt_show', slug=slug)

    context = {'receipt': receipt, 'invoices': invoices}
    return render(request, 'isis/createviews/receipt_invoice.html', context=context)


def check_costumer_invoices(costumer):
    '''
    # Checks weather costumer has pending Invoices or not
    '''
    invoices = Invoice.objects.filter(costumer_id=int(costumer),
    paid_status=0, active_status=1, finished_status=1).order_by('date_created')

    if not invoices:
        return False
    
    return True

@login_required
def receipt_create_view(request):
    print(request)

    if request.method == 'POST':
        costumer = request.POST.get('costumer')
        if not costumer:
            messages.warning(request, _("There are no invoices with pending payments! Please create Invoice First."))
            return redirect('isis:invoice_create')
        
        costumer_invoices = check_costumer_invoices(costumer)

        # Checks weather costumer has pending Invoices or not
        if not costumer_invoices:
            messages.warning(request, _("This costumer has no pending invoices!"))
            return redirect('isis:receipt_list')

        form = ReceiptForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance.credit = 0
            instance.debit = 0

            document_number = increment_invoice_number(Receipt)

            instance.number = document_number
            name = '{} {}'.format(_('Receipt'), document_number)
        
            instance.name = name
            slug = slugify(name)
            instance.slug = slugify(name)
            instance = instance.save()
            
            messages.success(request, _("Receipt created successfully!"))

            return redirect('isis:receipt_invoice', slug=slug)
            
        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:receipt_create')
    else:
        form = ReceiptForm()
        context = {'form': form}
        return render(request, 'isis/createviews/receipt_create.html', context)


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


@login_required
def receipt_detail_view(request, slug):
    receipt = get_object_or_404(Receipt, slug=slug)
    invoice_items = ReceiptInvoice.objects.filter(receipt=receipt)

    # Field totals
    total = invoice_items.aggregate(total=Coalesce(Sum('debit'), V(0), output_field=DecimalField()))
    total_paid = invoice_items.aggregate(total=Coalesce(Sum('paid'), V(0), output_field=DecimalField()))
    total_debt = invoice_items.aggregate(total=Coalesce(Sum('remaining'), V(0), output_field=DecimalField()))

    context ={}
    # add the dictionary during initialization
    context["receipt"] = receipt    
    context["invoices"] = invoice_items
    context["total"] = total
    context["total_paid"] = total_paid
    context["total_debt"] = total_debt

    return render(request, "isis/detailviews/receipt_detail_view.html", context)


########################## Document ##########################
class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'isis/listviews/document_list.html'


@login_required
def document_create_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Document added successfully!"))

            if request.POST.get('save_document'):
                return redirect('isis:document_list')
            else:
                return redirect('isis:document_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:document_create')
    else:
        form = DocumentForm()
        context = {'form': form}
        return render(request, 'isis/createviews/document_create.html', context)


@login_required
def document_update_view(request, slug):
    document = get_object_or_404(Document, slug=slug)
    form = DocumentForm(request.POST or None, instance=document)

    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Document updated successfully!"))

            if request.POST.get('save_document'):
                return redirect('isis:document_list')
            else:
                return redirect('isis:document_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:document_update', slug=slug)

    context = {'form': form}
    return render(request, 'isis/updateviews/document_update.html', context)


@login_required
def document_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Document.objects.filter(id__in=selected_ids).delete()
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:document_list')
        
        messages.warning(request, _("Document delete successfully!"))
        return redirect('isis:document_list')


@login_required
def document_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    document = get_object_or_404(Document, slug=slug)

    context ={}
    # add the dictionary during initialization
    context["document"] = document    
    return render(request, "isis/detailviews/document_detail_view.html", context)


@login_required
def invoicing_list_view(request):

    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    if request.method == "POST":
        search_form = StockSearchForm(request.POST)
        start_date = request.POST.get("start_date".replace('T', " "))
        end_date = request.POST.get("end_date")

        invoicing = Invoicing.objects.raw("""
        SELECT inv.*, SUM(item.discount_total) AS ds, SUM(item.sub_total) AS sb, 
        SUM(item.tax_total) AS tax, SUM(item.total) AS tt 
        FROM isis_invoicing AS inv
        LEFT JOIN isis_invoicingitem item ON inv.id=item.invoicing_id
        WHERE inv.date_created BETWEEN '{}' AND '{}'
        GROUP BY inv.id  
        """.format(str(start_date).replace('T', " "), str(end_date).replace('T', " ")))
    else:
        search_form = StockSearchForm()
        invoicing = Invoicing.objects.raw("""
        SELECT inv.*, SUM(item.discount_total) AS ds, SUM(item.sub_total) AS sb, 
        SUM(item.tax_total) AS tax, SUM(item.total) AS tt 
        FROM isis_invoicing AS inv
        LEFT JOIN isis_invoicingitem item ON inv.id=item.invoicing_id
        WHERE inv.date_created BETWEEN '{}' AND '{}'
        GROUP BY inv.id  """.format(start_date, end_date))
    
    context = {}
    context['search_form'] = search_form
    context['object_list'] = invoicing

    return render(request, 'isis/listviews/invoicing_list.html', context) 


@login_required
def invoicing_create_view(request):
    if request.method == 'POST':
        form = InvoicingForm(request.POST)
        costumer_form = CostumerForm(request.POST)
        warehouse_form = WarehouseForm(request.POST)
        payment_term_form = PaymentTermForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST)
        document_form = DocumentForm(request.POST)

        if request.POST.get('save_costumer') is not None \
            or request.POST.get('save_costumer_new') is not None:
            print(costumer_form.is_valid())

            if costumer_form.is_valid():
                instance = costumer_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                if request.POST.get('parent') is None or request.POST.get('parent') == "":
                    instance.parent = 0
                else:
                    instance.parent = int(request.POST.get('parent'))
                instance = instance.save()

                return redirect('isis:invoicing_create')
            else:
                for error in costumer_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_create')

        if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
            if warehouse_form.is_valid():
                    instance = warehouse_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    if request.POST.get('parent') is None or request.POST.get('parent') == "":
                        instance.parent = 0
                    else:
                        instance.parent = int(request.POST.get('parent'))
                    instance = instance.save()

                    return redirect('isis:invoicing_create')
            else:
                for error in warehouse_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_create')

        if request.POST.get('save_payment_method') \
            or request.POST.get('save_payment_method_new'):
            if  payment_method_form.is_valid():
            
                    instance = payment_method_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    instance = instance.save()

                    return redirect('isis:invoicing_create')
            else:
                for error in payment_method_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_create')

        if request.POST.get('save_payment_term') or \
            request.POST.get('save_payment_term_new'):
            if payment_term_form.is_valid():
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoicing_create')
            else:
                for error in payment_term_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_create')
        
        if request.POST.get('save_document') or request.POST.get('save_document_new'):
            if document_form.is_valid():
                instance = document_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoicing_create')
            else:
                for error in document_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_create')
                
        if form.is_valid():

            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()

            document = request.POST.get('document')

            document_number = increment_document_number(Invoicing, int(document))

            instance.number = document_number

            name = '{} {}'.format(Document.objects.get(id=int(document)), document_number)
            instance.name = name
            slug = slugify(name)
            instance.slug = slug
            instance = instance.save()

            messages.success(request, _("Invoicing created successfully!"))

            return redirect('isis:invoicing_item_create', slug=slug)

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:invoicing_create')
    else:
        form = InvoicingForm()
        costumer_form = CostumerForm()
        warehouse_form = WarehouseForm()
        payment_term_form = PaymentTermForm()
        payment_method_form = PaymentMethodForm()
        document_form = DocumentForm()

        context = {'form': form, 'costumer_form': costumer_form, 
        'warehouse_form': warehouse_form, 'payment_term_form': payment_term_form,
        'payment_method_form': payment_method_form, 'document_form': document_form}
        return render(request, 'isis/createviews/invoicing_create.html', context)


@login_required
def invoicing_update_view(request, slug):
    invoicing = get_object_or_404(Invoicing, slug=slug)
    
    if invoicing.is_finished():
        messages.warning(request,_('Document is closed and cannot be edited.'))
        return redirect('isis:invoicing_list')

    form = InvoicingForm(request.POST or None, instance=invoicing)
    # Disable document select input
    form.fields['document'].disabled = True 

    costumer_form = CostumerForm(request.POST or None)
    warehouse_form = WarehouseForm(request.POST or None)
    payment_term_form = PaymentTermForm(request.POST or None)
    payment_method_form = PaymentMethodForm(request.POST or None)
    document_form = DocumentForm(request.POST or None)

    if request.method == 'POST':
        if request.POST.get('save_costumer') is not None \
            or request.POST.get('save_costumer_new') is not None:
    
            if costumer_form.is_valid():
                instance = costumer_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                if request.POST.get('parent') is None or request.POST.get('parent') == "":
                    instance.parent = 0
                else:
                    instance.parent = int(request.POST.get('parent'))
                instance = instance.save()

                return redirect('isis:invoicing_update', slug=slug)
            else:
                for error in costumer_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_update', slug=slug)

        if request.POST.get('save_warehouse') or request.POST.get('save_warehouse_new'):
            if warehouse_form.is_valid():
                instance = warehouse_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                if request.POST.get('parent') is None or request.POST.get('parent') == "":
                    instance.parent = 0
                else:
                    instance.parent = int(request.POST.get('parent'))
                instance = instance.save()

                return redirect('isis:invoicing_update', slug=slug)
            else:
                for error in warehouse_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_update', slug=slug)

        if request.POST.get('save_payment_method') \
            or request.POST.get('save_payment_method_new'):
            if  payment_method_form.is_valid():
        
                instance = payment_method_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoicing_update', slug=slug)
            else:
                for error in payment_method_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_update', slug=slug)

        if request.POST.get('save_payment_term') or \
            request.POST.get('save_payment_term_new'):
            if payment_term_form.is_valid():
                instance = payment_term_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoicing_update', slug=slug)
            else:
                for error in payment_term_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_update', slug=slug)
        
        if request.POST.get('save_document') or request.POST.get('save_document_new'):
            if document_form.is_valid():
                instance = document_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()

                return redirect('isis:invoicing_update', slug=slug)
            else:
                for error in document_form.errors.values():
                    messages.error(request, error)
                return redirect('isis:invoicing_update', slug=slug)
                
        if form.is_valid():

            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()

            return redirect('isis:invoicing_item_create', slug=slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('isis:invoicing_update', slug=slug)

    context = {'form': form, 'costumer_form': costumer_form, 
        'warehouse_form': warehouse_form, 'payment_term_form': payment_term_form,
        'payment_method_form': payment_method_form, 'document_form': document_form}
    return render(request, 'isis/createviews/invoicing_create.html', context)


@login_required
def invoicing_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                try:
                    Invoicing.objects.filter(id__in=selected_ids).delete()
                    # Set parent to No parent in invoicing with deleted parents
                    Invoicing.objects.filter(parent__in=selected_ids).update(parent=0)
                except Exception as e:
                    messages.warning(request, _("Not Deleted! {}".format(e)))
                    return redirect('isis:invoicing_list')
        
        messages.warning(request, _("Invoicing delete successfully!"))
        return redirect('isis:invoicing_list')


def invoicing_dashboard_view(request):
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    last_invoicings =  Invoicing.objects.all().order_by('-date_created')[:15]
    total_invoicings =  Invoicing.objects.all().count()
    all_invoicings = Invoicing.objects.all().order_by('name')
    
    context = {}
    context['total'] = total_invoicings
    context['last'] = last_invoicings
    context['all'] = all_invoicings
    
    return render(request, 'isis/dashboardviews/invoicing_dashboard.html', context=context)

@login_required
def invoicing_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    invoicing = get_object_or_404(Invoicing, slug=slug)
    payments = ReceiptInvoicing.objects.filter(invoicing=invoicing)

    total_payment = [Invoicing.objects.filter(id=i.invoicing_id) for i in payments]

    total = total_payment[0].aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))
    total_paid = payments.aggregate(total=Coalesce(Sum('paid'), V(0), output_field=DecimalField()))
    total_debt = payments.aggregate(total=Coalesce(Sum('remaining'), V(0), output_field=DecimalField()))

    paid_invoicings = Invoicing.objects.filter(costumer=invoicing.costumer, 
    paid_status=1).exclude(id=invoicing.id).order_by('-number')[:5]
    
    overdue_invoicings = Invoicing.objects.filter(costumer=invoicing.costumer, 
    paid_status=0, due_date__lt=datetime.datetime.now()).exclude(id=invoicing.id).order_by('number')
    
    not_paid_invoicings = Invoicing.objects.filter(costumer=invoicing.costumer, 
    paid_status=0).exclude(id=invoicing.id).order_by('number')
    
    context ={}
    # add the dictionary during initialization
    context["invoicing"] = invoicing    
    context["paid_invoicings"] = paid_invoicings     
    context["not_paid_invoicings"] = not_paid_invoicings     
    context["overdue_invoicings"] = overdue_invoicings     
    context["payments"] = payments
    context["total"] = total
    context["total_paid"] = total_paid
    context["total_debt"] = total_debt
    
    return render(request, "isis/detailviews/invoicing_detail_view.html", context)


@login_required
def invoicing_item_delete_view(request):
    
    if request.is_ajax():
        selected_ids = request.POST['check_box_item_ids']
        selected_ids = json.loads(selected_ids)
        
        print(selected_ids)
        if len(selected_ids) == 1 and selected_ids[0] == 'None':
            return redirect('isis:invoicing_item_create')

        if len(selected_ids) > 1:
            item = InvoicingItem.objects.filter(id=int(selected_ids[1])).first()
        else:
            item = InvoicingItem.objects.filter(id=int(selected_ids[0])).first()

        try:
            InvoicingItem.objects.filter(id__in=selected_ids).delete()
            increase_decrease_invoicing_totals(item.invoicing_id)
        except Exception as e:
            messages.warning(request, _("Not Deleted! {}.".format(e)))
            print(e)
            return redirect('isis:invoicing_create')
        return redirect('isis:invoicing_create')


@login_required
def invoicing_item_create_view(request, slug):
    """
    Creates or Adds Invoicing Items
    """
    invoicing = get_object_or_404(Invoicing, slug=slug)
    
    if invoicing.is_finished():
        messages.warning(request,_('Document is closed and cannot be edited.'))
        return redirect('isis:invoicing_list')

    items = InvoicingItem.objects.filter(invoicing=invoicing)

    tax_total = items.aggregate(tax=Coalesce(Sum('tax_total'), V(0), output_field=DecimalField()))
    discount_total = items.aggregate(discount=Coalesce(Sum('discount_total'), V(0), output_field=DecimalField()))
    sub_total = items.aggregate(subtotal=Coalesce(Sum('sub_total'), V(0), output_field=DecimalField()))
    total = items.aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))

    if request.method == 'POST':
        form = InvoicingItemForm(request.POST)

        if request.POST.get('validate'):
            document = '{} - {}'.format(_('Invoicing'), invoicing.id)

            # Records stock movement 
            if invoicing.finished_status == 0:
                for i in items:
                    manage_stock(request, document, i.product, -i.quantity, invoicing.warehouse, invoicing.costumer, 
                "Costumer Invoicing")
            
            # Changes the Invoicing status to finished_status
            inv = Invoicing.objects.filter(id=invoicing.id).update(finished_status=1)
            
            if invoicing.document.track_payment == 1:
                return redirect('isis:document_payment', slug=slug)
            else:
                return redirect('isis:invoicing_show', slug=slug)         
        else:
            # Records a line to Invoicing
            name = request.POST.get('product')
            quantity = Decimal(request.POST.get('quantity'))
            tax = Decimal(request.POST.get('tax'))
            discount = Decimal(request.POST.get('discount'))
            price = Decimal(request.POST.get('price'))
            warehouse = invoicing.warehouse

            # Gets or saves the product information
            product_object = get_or_save_product(request, name, tax, warehouse)
            print(product_object)

            if not product_object:
                return redirect('isis:invoicing_item_create', slug=slug)

            # save the data and after fetch the object in instance
            instance = InvoicingItem(invoicing=invoicing, tax=tax, quantity=quantity,
            discount= discount, price=price, product=product_object) 
            instance.save()
            
            increase_decrease_invoicing_totals(invoicing.id)

        return redirect('isis:invoicing_item_create', slug=slug)
    else:
        form = InvoicingItemForm(None)
        return render(request, 'isis/createviews/invoicing_item_create.html', 
        {'invoicing': invoicing, 'form': form, 'items': items, 'tax_total': tax_total, 
        'discount_total': discount_total, 'sub_total': sub_total, 'total': total})


@login_required
def invoicing_show(request, slug):
    """
    Displays Invoicing for printing, export, ...
    """
    invoicing = get_object_or_404(Invoicing, slug=slug)
    items = InvoicingItem.objects.filter(invoicing=invoicing)

    tax_total = items.aggregate(Sum('tax_total'))
    discount_total = items.aggregate(Sum('discount_total'))
    sub_total = items.aggregate(Sum('sub_total'))
    total = items.aggregate(Sum('total'))

    costumer = Costumer.objects.get(id=invoicing.costumer.id)
    company = Settings.objects.first()

    context = {'invoicing': invoicing, 'items': items, 'tax_total': tax_total, 
    'discount_total': discount_total, 'sub_total': sub_total, 
    'total': total, 'costumer': costumer, 'company': company}

    instance = Invoicing.objects.filter(id=invoicing.id).update(finished_status=1)
    return render(request, 'isis/documents/invoicing.html', context) 


def increase_decrease_invoicing_totals(invoicing_id):
    """
    Modifies (Decreases or increases) Invoicing totals when item is deleted
    """

    items = InvoicingItem.objects.filter(invoicing=invoicing_id)

    tax_total = items.aggregate(tax=Coalesce(Sum('tax_total'), V(0), output_field=DecimalField()))
    discount_total = items.aggregate(discount=Coalesce(Sum('discount_total'), V(0), output_field=DecimalField()))
    sub_total = items.aggregate(subtotal=Coalesce(Sum('sub_total'), V(0), output_field=DecimalField()))
    total = items.aggregate(total=Coalesce(Sum('total'), V(0), output_field=DecimalField()))

    inv = Invoicing.objects.filter(id=invoicing_id).update(
    debit=total['total'],
    total=total['total'],
    subtotal=sub_total['subtotal'],
    total_tax=tax_total['tax'],
    total_discount=discount_total['discount']
    )

    return inv


def document_payment_view(request, slug):
    invoicing = get_object_or_404(Invoicing, slug=slug)
    payment_method = PaymentMethod.objects.filter(active_status=1)

    if request.method == "POST":
        data = dict(request.POST)

        print(request.POST)

        i = 0
        for d in data['amount']:
            
            # compute Total paid amount 
            # Get the list containing the total paid amount
            l = data['amount']
            t = sum([Decimal(i) for i in l if i.isdecimal()])
            
            if t < Decimal(invoicing.total):
                messages.error(request, _('Paid amount is less than total, it must be equal to total amount.'))
                return redirect('isis:document_payment', slug=slug)
            elif t > Decimal(invoicing.total):
                messages.error(request, _('Paid amount is more than total, it must be equal to total amount.'))
                return redirect('isis:document_payment', slug=slug)

            # if theres a payment amount entered in input
            if d:
                notes = data['notes'][i]
                file = data['file'][i]
                payment_method_ = PaymentMethod.objects.filter(id=int(data['payment_id'][i])).first()

                print(i)
                print(data['payment_id'][i])

                payment = DocumentPayment.objects.create(invoicing=invoicing, 
                payment_method=payment_method_, amount=Decimal(d), 
                notes=notes, file=file)
                
                i += 1

        # We a going to use date_modified for payment date
        Invoicing.objects.filter(id=invoicing.id).update(date_modified= datetime.datetime.now(), 
        finished_status=1, paid_status=1, debit=0, credit=invoicing.total)

        messages.success(request, _("Payment entered successfully"))
        invoicing_show(request, slug)
        return redirect('isis:invoicing_show', slug=slug)

    context = {}
    context['invoicing'] = invoicing
    context['payment_method'] = payment_method

    return render(request, 'isis/modals/document_payment_modal.html', context)

