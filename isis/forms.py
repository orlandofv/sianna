import datetime

import sys
from turtle import onclick
from django import forms
from .models import (Product, Gallery, Tax, Warehouse)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AccordionGroup, TabHolder, Tab
from django.utils.translation import ugettext_lazy as _
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from django.utils import timezone

from users.models import User

from asset_app.fields import ListTextWidget


class ProductForm(forms.ModelForm):
    code = forms.CharField(max_length=50)
    name = forms.CharField(max_length=255)
    parent = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)
    tax = forms.ModelChoiceField(queryset=Tax.objects.all())
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), label=_('Default Warehouse'))
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
                    Column('barcode', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('parent', css_class='form-group col-md-6 mb-0'),
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

    def clean_parent(self):
        pass

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


class WarehouseForm(forms.ModelForm):

    parent = forms.ModelChoiceField(queryset=Warehouse.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(WarehouseForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "warehouse-form-id"
        self.helper.form_class = "warehouse-form-class"
        self.helper.layout = Layout(
        HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add/Update Warehouse'),)),
        BS5Accordion(
            AccordionGroup(_('WAREHOUSE MAIN DATA'),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('parent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
                Row(
                    Column('address', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
                ),
                Row(
                    Column('contacts', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
                ),
                
                Row(
                    Column('active_status', css_class='form-group col-md-6 mb-0'),
                    Column('open_status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
                Row(
                    Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
                
                Row(
                    Column('notes', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'),
            ),
                HTML('<br>'),
                Submit('save_warehouse', _('Save & Close'), css_class='btn btn-primary fas fa-save'),
                Submit('save_warehouse_new', _('Save & Edit'), css_class='btn btn-primary fas fa-save'),
                Reset('reset', 'Clear', css_class='btn btn-danger'),
                flush=True,
                always_open=True),
        )
    
    def clean_parent(self):
        pass

    class Meta:
        model = Warehouse
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')

