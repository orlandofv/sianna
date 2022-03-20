from lib2to3.pgen2.token import RIGHTSHIFTEQUAL
from turtle import onclick
from django import forms
from .models import (Component, MaintenanceSchedule, Maintenance, 
Company, Division, Branch, Position, ComponentAllocation, Group, System, Type, SubType, Vendor)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AccordionGroup
from django.utils.translation import ugettext_lazy as _
from crispy_bootstrap5.bootstrap5 import BS5Accordion
from django.utils import timezone

class ComponentForm(forms.ModelForm):
    """Form definition for Component."""
    
    component_system_no = forms.IntegerField(widget=forms.NumberInput, label=_('System No.'),)
    component_name = forms.CharField(widget=forms.TextInput, label=_('Component Name'))
    component_manufacturer = forms.CharField(label=_('Manufacturer'))
    component_stock_code = forms.CharField(label=_('Stock Code'))
    maintenance_schedule= forms.ModelChoiceField(queryset=MaintenanceSchedule.objects.all(),
    label=_('Maintenance Schedule'))
    component_image = forms.ImageField(label=_('Image'), initial="default.jpeg", 
    widget=forms.FileInput(), required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
             HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Component'),)),
            BS5Accordion(
        AccordionGroup(_('Component Data'),
                Row(
                    Column('component_system_no', css_class='form-group col-md-6 mb-0'),
                    Column('component_name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('component_manufacturer', css_class='form-group col-md-6 mb-0'),
                    Column('component_stock_code', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                "component_image"),
        AccordionGroup(_('Maintenance Schedule'),
            FieldWithButtons('maintenance_schedule', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop"))),
            flush=True,
            always_open=True),
            'notes',
            Submit('submit', 'Save and Close'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )

    class Meta:
        """Meta definition for Componentform."""

        model = Component
        fields = ("component_system_no", "component_name","component_manufacturer", "component_stock_code",
        "maintenance_schedule","component_image","notes",)


class MaintenanceForm(forms.ModelForm):
    ROUTINE = 1
    PREVENTIVE = 2
    CORRECTIVE = 3
    PREDECTIVE = 4

    MAINTENANCE_CHOICES = (
        (ROUTINE, 'Routine'), 
        (PREVENTIVE, 'Preventive'), 
        (CORRECTIVE, 'Corrective'), 
        (PREDECTIVE, 'Predective'), 
    )

    HOURS = 1
    DAYS = 2
    MONTHS = 3
    KM = 4

    MAINTENANCE_SCHEDULE = (
        (HOURS, 'Hours'), (DAYS, 'Days'), (MONTHS, 'Months'), 
        (KM, 'KM\'s'), 
    )
    maintenance_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    maintenance_type = forms.ChoiceField(choices=MAINTENANCE_CHOICES)
    maintenance_schedule = forms.ChoiceField(choices=MAINTENANCE_SCHEDULE)
    maintenance_frequency = forms.IntegerField(widget=forms.NumberInput)
    time_allocated = forms.FloatField(widget=forms.NumberInput)
    maintenance_action = forms.CharField(widget=forms.TextInput, max_length=255)
    item_used = forms.CharField(widget=forms.TextInput, max_length=20)
    quantity = forms.FloatField(widget=forms.NumberInput)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Maintenance'),)),
            BS5Accordion(
            AccordionGroup(_('Maintenance Data'),
            Row(Column('maintenance_name', css_class='form-group col-md-12 mb-0'),),
            Row(
                Column('maintenance_schedule', css_class='form-group col-md-3 mb-0'),
                Column('maintenance_frequency', css_class='form-group col-md-3 mb-0'),
                Column('maintenance_type', css_class='form-group col-md-3 mb-0'),
                Column('time_allocated', css_class='form-group col-md-3 mb-0'),

            ),
            Row(
                Column('maintenance_action', css_class='form-group col-md-12 mb-0'),),
            Row(
                Column('item_used', css_class='form-group col-md-10'),
                Column('quantity', css_class='form-group col-md-2')
            ),
            Row(Column('notes', css_class='form-group col-md-12')),
            flush=True,
            always_open=True)
            ),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )

    def clean(self):
        super(MaintenanceForm, self).clean()

        maintenance_frequency = self.cleaned_data.get('maintenance_frequency')
        time_allocated = self.cleaned_data.get('time_allocated')
        quantity = self.cleaned_data.get('quantity')

        if maintenance_frequency <= 0:
            self.errors['maintenance_frequency'] = self.error_class([_('Maintenance frequency must be ' 
            'greater than zero')])
        
        return self.cleaned_data

    class Meta:
        model = Maintenance
        exclude = ('date_created', 'date_modified', 'slug')


class MaintenanceScheduleForm(forms.ModelForm):
    schedule_name = forms.CharField(widget=forms.TextInput, max_length=50)
    maintenance_name = forms.ModelChoiceField(queryset=Maintenance.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(MaintenanceScheduleForm, self).__init__(*args,)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Maintenance Schedule'),)),
            BS5Accordion(
            AccordionGroup(_('Schedule Data'),
            Row(Column('schedule_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('maintenance_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = MaintenanceSchedule
        exclude = ('date_created', 'date_modified', 'slug')


class CompanyForm(forms.ModelForm):
    company_name = forms.CharField(label=_('Company Name'), 
    widget=forms.TextInput, max_length=100)
    company_address = forms.CharField(required=False, max_length=255)
    company_contacts = forms.CharField(required=False, max_length=255)
    company_manager = forms.CharField(max_length=100, required=False)
    company_email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Company'),)),
            BS5Accordion(
            AccordionGroup(_('Company Data'),
            Row(Column('company_name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('company_address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('company_contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('company_manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('company_email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Company
        exclude = ('date_created', 'date_modified', 'slug')


class DivisionForm(forms.ModelForm):
    division_name = forms.CharField(label=_('Division Name'), 
    widget=forms.TextInput, max_length=100)
    company_name = forms.ModelChoiceField(label=_('Company Name'), queryset=Company.objects.all())
    division_address = forms.CharField(required=False, max_length=255)
    division_contacts = forms.CharField(required=False, max_length=255)
    division_manager = forms.CharField(max_length=100, required=False)
    division_email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Division'),)),
            BS5Accordion(
            AccordionGroup(_('Division Data'),
            Row(Column('division_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('company_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('division_address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('division_contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('division_manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('division_email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Division
        exclude = ('date_created', 'date_modified', 'slug')


class BranchForm(forms.ModelForm):
    branch_name = forms.CharField(label=_('Branch Name'), 
    widget=forms.TextInput, max_length=100)
    division_name = forms.ModelChoiceField(label=_('Division Name'), queryset=Division.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Branch'),)),
            BS5Accordion(
            AccordionGroup(_('Branch Data'),
            Row(Column('branch_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('division_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Branch
        exclude = ('date_created', 'date_modified', 'slug')


class PositionForm(forms.ModelForm):
    position_name = forms.CharField(label=_('Position Name'), 
    widget=forms.TextInput, max_length=100)
    branch_name = forms.ModelChoiceField(label=_('Branch Name'), queryset=Branch.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Position'),)),
            BS5Accordion(
            AccordionGroup(_('Position Data'),
            Row(Column('position_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('branch_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Position
        exclude = ('date_created', 'date_modified', 'slug')


class GroupForm(forms.ModelForm):
    group_name = forms.CharField(label=_('Group Name'), 
    widget=forms.TextInput, max_length=100)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Group'),)),
            BS5Accordion(
            AccordionGroup(_('Group Data'),
            Row(Column('group_name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Group
        exclude = ('date_created', 'date_modified', 'slug')


class SystemForm(forms.ModelForm):
    system_name = forms.CharField(label=_('System Name'), 
    widget=forms.TextInput, max_length=100)
    group_name = forms.ModelChoiceField(queryset=Group.objects.all(), label=_('Group Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New System'),)),
            BS5Accordion(
            AccordionGroup(_('System Data'),
            Row(Column('system_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('group_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = System
        exclude = ('date_created', 'date_modified', 'slug')


class TypeForm(forms.ModelForm):
    type_name = forms.CharField(label=_('Type Name'), 
    widget=forms.TextInput, max_length=100)
    system_name = forms.ModelChoiceField(queryset=System.objects.all(), label=_('System Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Type'),)),
            BS5Accordion(
            AccordionGroup(_('Type Data'),
            Row(Column('type_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('system_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Type
        exclude = ('date_created', 'date_modified', 'slug')


class SubTypeForm(forms.ModelForm):
    subtype_name = forms.CharField(label=_('SubType Name'), 
    widget=forms.TextInput, max_length=100)
    type_name = forms.ModelChoiceField(queryset=Type.objects.all(), label=_('Type Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(SubTypeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New SubType'),)),
            BS5Accordion(
            AccordionGroup(_('SubType Data'),
            Row(Column('subtype_name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('type_name', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = SubType
        exclude = ('date_created', 'date_modified', 'slug')


class ComponentAllocationForm(forms.ModelForm):
    
    GOOD = 1
    BROKEN = 0

    STATUS = ((GOOD, 'Good'), (BROKEN, 'Broken'),)

    component_name = forms.ModelChoiceField(queryset=Component.objects.all(), label=_('component Name'))
    vendor_name = forms.ModelChoiceField(queryset=Vendor.objects.all(),)
    company_name = forms.ModelChoiceField(queryset=Company.objects.all())
    division_name = forms.ModelChoiceField(queryset=Division.objects.all())
    branch_name = forms.ModelChoiceField(queryset=Branch.objects.all())
    position_name = forms.ModelChoiceField(queryset=Position.objects.all())
    component_serial_number = forms.CharField(label=_('Component Serial No.'), max_length=50)
    component_status = forms.ChoiceField(label=_('Component Status'), choices=STATUS, 
    initial=GOOD)
    component_image = forms.ImageField(label=_('Image'), initial="default.jpeg")
    purchase_amount = forms.DecimalField(widget=forms.NumberInput, initial=0, max_digits=9, decimal_places=2)
    date_purchased = forms.DateTimeField(widget=forms.DateTimeInput, initial=timezone.now)
    date_allocated = forms.DateTimeField(widget=forms.DateTimeInput, initial=timezone.now)
    depreciation = forms.FloatField(label=_('Depreciation %'), initial=0)
    start_value_hours = forms.FloatField(label=_('Start Value (Hours)'), initial=0)
    start_value_years = forms.FloatField(label=_('Years'), initial=0)
    start_value_milliege = forms.FloatField(label=_('KM'), initial=0)
    garrantee_value_hours = forms.FloatField(label=_('Warrantee Value (Hours)'), initial=0)
    garrantee_value_years = forms.FloatField(label=_('Years'), initial=0)
    garrantee_milliege = forms.FloatField(label=_('KM'), initial=0)
    end_of_life_hours = forms.FloatField(label=_('End of Life (Hours)'), initial=0)
    end_of_life_years = forms.FloatField(label=_('Years'),initial=0)
    end_of_life_milliege = forms.FloatField(label=_('KM'),initial=0)
    warn_before_hours = forms.FloatField(label=_('Warn Before (Hours)'), initial=0)
    warn_before_years = forms.FloatField(label=_('Years'), initial=0)
    warn_before_milliege = forms.FloatField(label=_('KM'), initial=0)
    group_name = forms.ModelChoiceField(queryset=Group.objects.all())
    system_name = forms.ModelChoiceField(queryset=System.objects.all())
    type_name = forms.ModelChoiceField(queryset=Type.objects.all())
    subtype_name = forms.ModelChoiceField(queryset=SubType.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(ComponentAllocationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Component Allocation'),)),
            BS5Accordion(
            AccordionGroup(_('ALLOCATE COMPONENT'),
                FieldWithButtons('component_name', StrictButton('',  css_class="btn fa fa-plus",
                data_bs_toggle="modal", data_bs_target="#component"), css_class='form-group col-md-12 mb-0'),
                Row(
                    FieldWithButtons('vendor_name', StrictButton('',  css_class="btn fa fa-plus",
                    data_bs_toggle="modal", data_bs_target="#staticBackdrop"), 
                    css_class='form-group col-md-6 mb-0'),
                    Column('component_serial_number', css_class='form-group col-md-6 mb-0'),
                ),
                Row(Column('component_image', css_class='form-group col-md-12 mb-0'),),
                Row(
                    Column('date_purchased', css_class='form-group col-md-4 mb-0'),
                    Column('purchase_amount', css_class='form-group col-md-4 mb-0'),
                    Column('date_allocated', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('start_value_hours', css_class='form-group col-md-4 mb-0'),
                    Column('start_value_years', css_class='form-group col-md-4 mb-0'),
                    Column('start_value_milliege', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('garrantee_value_hours', css_class='form-group col-md-4 mb-0'),
                    Column('garrantee_value_years', css_class='form-group col-md-4 mb-0'),
                    Column('garrantee_milliege', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('end_of_life_hours', css_class='form-group col-md-4 mb-0'),
                    Column('end_of_life_years', css_class='form-group col-md-4 mb-0'),
                    Column('end_of_life_milliege', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('warn_before_hours', css_class='form-group col-md-4 mb-0'),
                    Column('warn_before_years', css_class='form-group col-md-4 mb-0'),
                    Column('warn_before_milliege', css_class='form-group col-md-4 mb-0'),
                ),
                Row(Column('depreciation', css_class='form-group col-md-4 mb-0'),),
            ),
            AccordionGroup(_('ATTACH TO SYSTEM'),
                Row(
                        FieldWithButtons('group_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#group"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('system_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#system"), css_class='form-group col-md-6 mb-0'),
                    ),
                Row(
                        FieldWithButtons('type_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#type"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('subtype_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#subtype"), css_class='form-group col-md-6 mb-0'),

                    ),
            ),
            AccordionGroup(_('ATTACH TO LOCATION'),
                Row(
                        FieldWithButtons('company_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#company"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('division_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#division"), css_class='form-group col-md-6 mb-0'),
                    ),
                Row(
                        FieldWithButtons('branch_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#branch"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('position_name', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#position"), css_class='form-group col-md-6 mb-0'),
                    ),   
            ),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            flush=True,
            always_open=True),
            Submit('submit', ('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = ComponentAllocation
        exclude = ('date_created', 'date_modified', 'slug')


class VendorForm(forms.ModelForm):
    vendor_name = forms.CharField(label=_('Vendor Name'), 
    widget=forms.TextInput, max_length=100)
    vendor_address = forms.CharField(required=False, max_length=255)
    vendor_contacts = forms.CharField(required=False, max_length=255)
    vendor_manager = forms.CharField(max_length=100, required=False)
    vendor_email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Vendor'),)),
            BS5Accordion(
            AccordionGroup(_('Vendor Data'),
            Row(Column('vendor_name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('vendor_address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('vendor_contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('vendor_manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('vendor_email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('submit', _('Save & Close'),),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Vendor
        exclude = ('date_created', 'date_modified', 'slug')

