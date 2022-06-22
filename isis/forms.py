from dataclasses import Field
import datetime
from itertools import product
from math import prod

import sys
from turtle import onclick
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AccordionGroup, TabHolder, Tab
from django.utils.translation import ugettext_lazy as _
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from .models import (Product, Gallery, Tax, Invoice, InvoiceItem, 
PaymentTerm, PaymentMethod, Receipt, Category)
from warehouse.models import Warehouse
from django.utils import timezone
from users.models import User

from asset_app.fields import ListTextWidget


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(label=_('Parent Category'), 
    queryset=Category.objects.filter(active_status=1), 
    required=False, initial=0)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "category-form-id"
        self.helper.form_class = "category-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Category'),)),
        BS5Accordion(
            AccordionGroup(_('CATEGORY MAIN DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('parent', css_class='form-group col-md-3 mb-0'),
                    Column('active_status', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('image', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_category', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_category_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = Category
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


    def clean_parent(self):
        pass


class ProductForm(forms.ModelForm):
    code = forms.CharField(max_length=50)
    name = forms.CharField(max_length=255)
    tax = forms.ModelChoiceField(queryset=Tax.objects.all(), initial=1)
    barcode = forms.CharField(max_length=255, required=False)
    sell_price = forms.DecimalField(label=_('Selling Prince'), max_digits=18, decimal_places=6, initial=0, required=False)
    min_sell_price = forms.DecimalField(label=_('Min. Selling Prince'),max_digits=18, decimal_places=6, initial=0, required=False)
    sell_price2 = forms.DecimalField(label=_('Selling Prince 2'), max_digits=18, decimal_places=6, initial=0, required=False)
    sell_price3 = forms.DecimalField(label=_('Selling Prince 3'), max_digits=18, decimal_places=6, initial=0, required=False)
    sell_price4 = forms.DecimalField(label=_('Selling Prince 4'), max_digits=18, decimal_places=6, initial=0, required=False)
    sell_price5 = forms.DecimalField(label=_('Selling Prince 5'), max_digits=18, decimal_places=6, initial=0, required=False)
    purchase_price = forms.DecimalField(label=_('Purchase Price'), max_digits=18, decimal_places=6, initial=0, required=False)
    physical_stock = forms.DecimalField(label=_('Purchase Price'), max_digits=18, decimal_places=6, initial=0, required=False)
    stock_limit = forms.DecimalField(label=_('Stock Limit'), max_digits=18, decimal_places=6, initial=0, required=False)
    desired_stock = forms.DecimalField(label=_('Desired Stock'), max_digits=18, decimal_places=6, initial=0, required=False)
    # product_nature = forms.CharField(max_length=50, choices=PRODUCT_NATURE, initial=RAW_PRODUCT)
    product_url = forms.URLField(max_length=255, required=False)
    weight = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    length = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    width = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    height = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    # length_units = forms.CharField(max_length=10, choices=LENGTH_CHOICES, initial=M)
    area = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    # area_units = forms.CharField(max_length=10, choices=AREA_CHOICES, initial=M2)
    volume = forms.DecimalField(max_digits=9, decimal_places=6, initial=0, required=False)
    # volume_units = forms.CharField(max_length=10, choices=VOLUME_CHOICES, initial=0, required=False)
    # weight_units = forms.CharField(max_length=50, choices=WEIGHT_MEASUREMENT_CHOICES, initial=KG)
    # active_status = forms.IntegerField(choices=STATUSES, initial=ACTIVE)
    # sell_status = forms.IntegerField(choices=SELL_STATUSES, initial=FOR_SALE)
    # purchase_status = forms.IntegerField(choices=PURCHASE_STATUSES, initial=FOR_PURCHASE)
    images = forms.ImageField(label=_('Other Images'), required=False)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "product-form-id"
        self.helper.form_class = "product-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update product'),)),
        TabHolder(
            Tab(_('PRODUCT MAIN DATA'),
                Row(
                    Column('code', css_class='form-group col-md-6 mb-0'),
                    Column('barcode', css_class='form-group col-md-4 mb-0'),
                    Column('type', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    FieldWithButtons('category', StrictButton('',  css_class="btn fa fa-plus", 
                    data_bs_toggle="modal", data_bs_target="#category"), css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('sell_price', css_class='form-group col-md-3 mb-0'),
                    Column('min_sell_price', css_class='form-group col-md-3 mb-0'),
                    FieldWithButtons('tax', StrictButton('',  css_class="btn fa fa-plus", 
                    data_bs_toggle="modal", data_bs_target="#tax"), css_class='form-group col-md-3 mb-0'),
                    FieldWithButtons('warehouse', StrictButton('',  css_class="btn fa fa-plus", 
                    data_bs_toggle="modal", data_bs_target="#warehouse"), css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'),

                Row(
                    Column('description', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('sell_status', css_class='form-group col-md-3 mb-0'),
                    Column('purchase_status', css_class='form-group col-md-3 mb-0'),
                    Column('active_status', css_class='form-group col-md-3 mb-0'),
                    Column('product_nature', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('product_url', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),

            Tab(_('OTHER PRICES'),
                Row(
                    Column('sell_price2', css_class='form-group col-md-2 mb-0'),
                    Column('sell_price3', css_class='form-group col-md-2 mb-0'),
                    Column('sell_price4', css_class='form-group col-md-2 mb-0'),
                    Column('sell_price5', css_class='form-group col-md-2 mb-0'),
                    Column('purchase_price', css_class='form-group col-md-2 mb-0'),
                    Column('max_purchase_price', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row'),
            ),

            Tab(_('IMAGES'),
                Row(
                    Column('image', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('images', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
            Tab(_('AREA - VOLUME - WEIGHT'),
                Row(
                    Column('length', css_class='form-group col-md-2 mb-0'),
                    Column('width', css_class='form-group col-md-2 mb-0'),
                    Column('height', css_class='form-group col-md-2 mb-0'),
                    Column('length_units', css_class='form-group col-md-2 mb-0'),
                    Column('weight', css_class='form-group col-md-2 mb-0'),
                    Column('weight_units', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('area', css_class='form-group col-md-3 mb-0'),
                    Column('area_units', css_class='form-group col-md-3 mb-0'),
                    Column('volume', css_class='form-group col-md-3 mb-0'),
                    Column('volume_units', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'),
            ),
            Tab(_('STOCKS'),
                Row(
                    Column('min_stock', css_class='form-group col-md-3 mb-0'),
                    Column('desired_stock', css_class='form-group col-md-3 mb-0'),
                    Column('stock_limit', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'),
            ),
            Tab(_('PRIVATE NOTES'),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
        ),
         HTML('<br>'),
                Submit('save_product', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_product_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
        )

    def clean(self):
        cleaned_data = super().clean()

        code = cleaned_data.get('code')
        name = cleaned_data.get('name')
        
        if code == '':
            self.errors['code'] = self.error_class(_("""
            The Code of Product must not be empty."""))
    
        if name == '':
            self.errors['name'] = self.error_class(_("""
            The Name of Product must not be empty."""))
    
        return cleaned_data

    class Meta:
        model = Product
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class TaxForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaxForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "tax-form-id"
        self.helper.form_class = "tax-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Tax'),)),
        BS5Accordion(
            AccordionGroup(_('TAX MAIN DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('rate', css_class='form-group col-md-3 mb-0'),
                    Column('active_status', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_tax', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_tax_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = Tax
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class PaymentMethodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "payment_method-form-id"
        self.helper.form_class = "payment_method-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Payment Method'),)),
        BS5Accordion(
            AccordionGroup(_('PAYMENT METHOD DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_payment_method', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_payment_method_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = PaymentMethod
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class PaymentTermForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentTermForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "payment_term-form-id"
        self.helper.form_class = "payment_term-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Payment Term'),)),
        BS5Accordion(
            AccordionGroup(_('PAYMENT TERM DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_payment_term', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_payment_term_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = PaymentTerm
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class ReceiptForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "receipt-form-id"
        self.helper.form_class = "receipt-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Receipt'),)),
        BS5Accordion(
            AccordionGroup(_('RECEIPT DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_receipt', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_receipt_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = Receipt
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class InvoiceItemForm(forms.ModelForm):
    SERVICE = 'SERVICE'
    PRODUCT = 'PRODUCT'
    
    PRODUCT_CHOICES = ((SERVICE, _('Service')), (PRODUCT, _('Product')))
    type = forms.ChoiceField(choices=PRODUCT_CHOICES, initial=PRODUCT, required=False)

    data = [(x.rate, x.name) for x in Tax.objects.filter(active_status=1)]
    tax = forms.ChoiceField(choices=data)

    price = forms.DecimalField(max_digits=18, decimal_places=6, initial=0, 
    widget=forms.NumberInput(attrs={'autocomplete': "off"}))
    quantity = forms.DecimalField(max_digits=18, decimal_places=6, initial=0, widget=forms.TextInput)
    discount = forms.DecimalField(max_digits=4, decimal_places=2, initial=0, widget=forms.TextInput)
    invoice = forms.CharField(required=False)
    product = forms.ModelChoiceField(required=False, queryset=Product.objects.filter(active_status=1),
    widget=forms.Select(attrs={'class': 'product-select'}))


    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        
        self.fields['price'].widget = ListTextWidget(data_list=[], name='price_list')

        self.helper = FormHelper()
        self.helper.form_id = "invoice-items-form-id"
        self.helper.form_class = "form-inline"
        self.helper.layout = Layout(
        BS5Accordion(
            AccordionGroup(_('INVOICE ITEMS'),
            Row(
                Column('product', css_class='form-group col-md-4 mb-0'),
                Column('type', css_class='form-group col-md-2 mb-0'),
                Column('price', css_class='form-group col-md-2 mb-0'),
                Column('quantity', css_class='form-group col-md-1 mb-0'),
                Column('discount', css_class='form-group col-md-1 mb-0'),
                Column('tax', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'),
            
                Submit('add_item', _('Add Item'), css_class='btn btn-primary fa fa-plus-circle'),
        ),))
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        price = cleaned_data.get('price')
        discount = cleaned_data.get('discount')
        product = cleaned_data.get('product')
        
        try:
            pr = Product.objects.get(name=product)
            min_price = pr.min_sell_price

            if price < min_price:
                self.errors['price'] = self.error_class(_("""
                Price is lower than the product Minimum selling price {}.""".format(min_price)))

        except Product.DoesNotExist:
            min_price = 0

        if discount is None:
            self.errors['discount'] = self.error_class(_("""
            discount must be between 0 and 99.99."""))
        elif discount > 100 or discount < 0:
            self.errors['discount'] = self.error_class(_("""
            discount must be between 0 and 100."""))

    def clean_invoice(self):
        return None

    class Meta:
        model = InvoiceItem
        fields = "__all__"
        
class InvoiceForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=50)
    paid_status = forms.IntegerField(required=False, initial=0)
    delivered_status = forms.IntegerField(initial=0, required=False)
    finished_status = forms.IntegerField(initial=0, required=False)
    active_status = forms.IntegerField(initial=1, required=False)
    number = forms.IntegerField(initial=0, required=False)
        
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "invoice-form-id"
        self.helper.form_class = "invoice-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Invoice'),)),
        BS5Accordion(
            AccordionGroup(_('INVOICE DATA'),
                FieldWithButtons('costumer', StrictButton('',  css_class="btn fa fa-plus", 
                data_bs_toggle="modal", data_bs_target="#costumer"), css_class='form-group col-md-12 mb-0'),
                Row(
                    Column('date', css_class='form-group col-md-3 mb-0'),
                    Column('due_date', css_class='form-group col-md-3 mb-0'),
                    FieldWithButtons('warehouse', StrictButton('',  css_class="btn fa fa-plus", 
                    data_bs_toggle="modal", data_bs_target="#warehouse"), css_class='form-group col-md-6 mb-0'),
                ),
                Row(
                FieldWithButtons('payment_term', StrictButton('',  css_class="btn fa fa-plus", 
                data_bs_toggle="modal", data_bs_target="#payment_term"), css_class='form-group col-md-3 mb-0'),
                FieldWithButtons('payment_method', StrictButton('',  css_class="btn fa fa-plus", 
                data_bs_toggle="modal", data_bs_target="#payment_method"), css_class='form-group col-md-3 mb-0'),
                ),
                Column('notes', css_class='form-group col-md-12 mb-0'),
                Column('public_notes', css_class='form-group col-md-12 mb-0'),),
                HTML('<br>'),
                Submit('save_invoice', _('Next'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )

    class Meta:
        model = Invoice
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


