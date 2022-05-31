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

from django.utils import timezone
from users.models import User
from .models import (Product, Warehouse, Invoice, InvoiceItem, 
PaymentTerm, PaymentMethod)

from isis.models import Tax


from asset_app.fields import ListTextWidget

class InvoiceItemForm(forms.ModelForm):
    SERVICE = 'SERVICE'
    PRODUCT = 'PRODUCT'
    
    PRODUCT_CHOICES = ((SERVICE, _('Service')), (PRODUCT, _('Product')))
    type = forms.ChoiceField(choices=PRODUCT_CHOICES, initial=PRODUCT, required=False)

    data = [(x.rate, x.name) for x in Tax.objects.all()]
    tax = forms.ChoiceField(choices=data)

    price = forms.DecimalField(max_digits=18, decimal_places=6, initial=0, widget=forms.TextInput)
    quantity = forms.DecimalField(max_digits=18, decimal_places=6, initial=0, widget=forms.TextInput)
    discount = forms.DecimalField(max_digits=4, decimal_places=2, initial=0, widget=forms.TextInput)
    invoice = forms.CharField(required=False)
    product = forms.ModelChoiceField(required=False, queryset=Product.objects.filter(active_status=1))

    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget = ListTextWidget(data_list=Product.objects.all(), name='product')
        
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
                FieldWithButtons('supplier', StrictButton('',  css_class="btn fa fa-plus", 
                data_bs_toggle="modal", data_bs_target="#supplier"), css_class='form-group col-md-12 mb-0'),
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


