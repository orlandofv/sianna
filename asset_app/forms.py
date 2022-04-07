from lib2to3.pgen2.token import RIGHTSHIFTEQUAL
from turtle import onclick
from django import forms
from .models import (Component, MaintenanceSchedule, Maintenance, 
Company, Division, Branch, Position, Allocation, Group, System, Type, SubType, Vendor)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AccordionGroup
from django.utils.translation import ugettext_lazy as _
from crispy_bootstrap5.bootstrap5 import BS5Accordion
from django.utils import timezone


class ComponentForm(forms.ModelForm):
    """Form definition for Component."""
    
    component_no = forms.IntegerField(widget=forms.NumberInput, label=_('System No.'),)
    name = forms.CharField(widget=forms.TextInput, label=_('Component Name'))
    manufacturer = forms.CharField(label=_('Manufacturer'))
    stock_code = forms.CharField(label=_('Stock Code'))
    schedule= forms.ModelChoiceField(queryset=MaintenanceSchedule.objects.all(),
    label=_('Maintenance Schedule'))
    image = forms.ImageField(label=_('Image'), initial="default.jpeg", 
    widget=forms.FileInput(), required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        super(ComponentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "component-form-id"
        self.helper.form_class = "component-form-class"
        self.helper.layout = Layout(
             HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Component'),)),
            BS5Accordion(
        AccordionGroup(_('Component Data'),
                Row(
                    Column('component_no', css_class='form-group col-md-6 mb-0'),
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('manufacturer', css_class='form-group col-md-6 mb-0'),
                    Column('stock_code', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                "image"),
        AccordionGroup(_('Maintenance Schedule'),
            FieldWithButtons('schedule', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop"))),
            flush=True,
            always_open=True),
            'notes',
            Submit('save_component', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )

    class Meta:
        """Meta definition for Componentform."""

        model = Component
        fields = ("component_no", "name","manufacturer", "stock_code",
        "schedule","image","notes",)


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
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    type = forms.ChoiceField(choices=MAINTENANCE_CHOICES)
    schedule = forms.ChoiceField(choices=MAINTENANCE_SCHEDULE)
    frequency = forms.IntegerField(widget=forms.NumberInput, initial=1)
    time_allocated = forms.FloatField(widget=forms.NumberInput, initial=1)
    action = forms.CharField(widget=forms.TextInput, max_length=255)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.attrs = {"novalidate": ''}
        self.helper.form_id = "maintenance-form-id"
        self.helper.form_class = "maintenance-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Maintenance'),)),
            BS5Accordion(
            AccordionGroup(_('Maintenance Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            Row(
                Column('schedule', css_class='form-group col-md-3 mb-0'),
                Column('frequency', css_class='form-group col-md-3 mb-0'),
                Column('type', css_class='form-group col-md-3 mb-0'),
                Column('time_allocated', css_class='form-group col-md-3 mb-0'),

            ),
            Row(
                Column('action', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0')),
            Submit('save_maintenance', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Submit('save_maintenance_clone', _('Save and Clone'), css_class='btn btn-secondary fas fa-save'),
            Submit('save_maintenance_new', _('Save and New'), css_class='btn btn-success fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
            flush=True,
            always_open=True)
            ),
           
        )

    def clean(self):
        print('Executando o Clean')
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')

        name = cleaned_data.get('name')
        action = cleaned_data.get('action')
        time_allocated = cleaned_data.get('time_allocated')
       
        if frequency in (None, ""):
            self.errors['frequency'] = self.error_class([_('Maintenance frequency must not be ' 
            'empty.')])
        elif frequency <= 0:
            self.errors['frequency'] = self.error_class([_('Maintenance frequency must be ' 
            'greater than zero.')])

        if time_allocated in (None, ""):
            self.errors['time_allocated'] = self.error_class([_('Maintenance Time allocated must not be ' 
            'empty.')])

        elif time_allocated <= 0:
             self.errors['time_allocated'] = self.error_class([_('Maintenance Time allocated must be ' 
            'greater than zero.')])

        if name in (None, ""):
             self.errors['name'] = self.error_class([_('Maintenance name must no be ' 
            'empty.')])

        if action in (None, ""):
             self.errors['action'] = self.error_class([_('Maintenance Action must no be ' 
            'empty.')])

        return cleaned_data

    class Meta:
        model = Maintenance
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class MaintenanceScheduleForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput, max_length=50)
    maintenance = forms.ModelChoiceField(queryset=Maintenance.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(MaintenanceScheduleForm, self).__init__(*args,)

        self.helper = FormHelper(self)
        self.helper.form_id = "schedule-form-id"
        self.helper.form_class = "schedule-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Maintenance Schedule'),)),
            BS5Accordion(
            AccordionGroup(_('Schedule Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('maintenance', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_schedule', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = MaintenanceSchedule
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label=_('Company Name'), 
    widget=forms.TextInput, max_length=100)
    address = forms.CharField(required=False, max_length=255)
    contacts = forms.CharField(required=False, max_length=255)
    manager = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "company-form-id"
        self.helper.form_class = "company-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Company'),)),
            BS5Accordion(
            AccordionGroup(_('Company Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_company', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Company
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class DivisionForm(forms.ModelForm):
    name = forms.CharField(label=_('Division Name'), 
    widget=forms.TextInput, max_length=100)
    company = forms.ModelChoiceField(label=_('Company Name'), queryset=Company.objects.all())
    address = forms.CharField(required=False, max_length=255)
    contacts = forms.CharField(required=False, max_length=255)
    manager = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "division-form-id"
        self.helper.form_class = "division-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Division'),)),
            BS5Accordion(
            AccordionGroup(_('Division Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('company', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_division', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Division
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class BranchForm(forms.ModelForm):
    name = forms.CharField(label=_('Branch Name'), 
    widget=forms.TextInput, max_length=100)
    division = forms.ModelChoiceField(label=_('Division Name'), queryset=Division.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "branch-form-id"
        self.helper.form_class = "branch-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Branch'),)),
            BS5Accordion(
            AccordionGroup(_('Branch Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('division', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_branch', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Branch
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class PositionForm(forms.ModelForm):
    name = forms.CharField(label=_('Position Name'), 
    widget=forms.TextInput, max_length=100)
    branch = forms.ModelChoiceField(label=_('Branch Name'), queryset=Branch.objects.all())
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "position-form-id"
        self.helper.form_class = "position-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Position'),)),
            BS5Accordion(
            AccordionGroup(_('Position Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('branch', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_position', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Position
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class GroupForm(forms.ModelForm):
    name = forms.CharField(label=_('Group Name'), 
    widget=forms.TextInput, max_length=100)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "group-form-id"
        self.helper.form_class = "group-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Group'),)),
            BS5Accordion(
            AccordionGroup(_('Group Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_group', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Group
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class SystemForm(forms.ModelForm):
    name = forms.CharField(label=_('System Name'), 
    widget=forms.TextInput, max_length=100)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label=_('Group Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "system-form-id"
        self.helper.form_class = "system-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New System'),)),
            BS5Accordion(
            AccordionGroup(_('System Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('group', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_system', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = System
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class TypeForm(forms.ModelForm):
    name = forms.CharField(label=_('Type Name'), 
    widget=forms.TextInput, max_length=100)
    system = forms.ModelChoiceField(queryset=System.objects.all(), label=_('System Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "type-form-id"
        self.helper.form_class = "type-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Type'),)),
            BS5Accordion(
            AccordionGroup(_('Type Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('system', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_type', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Type
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class SubTypeForm(forms.ModelForm):
    name = forms.CharField(label=_('SubType Name'), 
    widget=forms.TextInput, max_length=100)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label=_('Type Name')) 
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(SubTypeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "subtype-form-id"
        self.helper.form_class = "subtype-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New SubType'),)),
            BS5Accordion(
            AccordionGroup(_('SubType Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            FieldWithButtons('type', StrictButton('',  css_class="btn fa fa-plus",
            data_bs_toggle="modal", data_bs_target="#staticBackdrop")),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_subtype', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = SubType
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class AllocationForm(forms.ModelForm):
    
    GOOD = 1
    BROKEN = 0

    STATUS = ((GOOD, 'Good'), (BROKEN, 'Broken'),)

    allocation_no = forms.IntegerField(label=('System No.'), widget=forms.NumberInput())
    component = forms.ModelChoiceField(queryset=Component.objects.all(), 
    label=_('Component Name'))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), label=_('Vendor Name'))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), label=_('Company Name'))
    division = forms.ModelChoiceField(queryset=Division.objects.all(), label=_('Division Name'))
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label=_('Branch Name'))
    position = forms.ModelChoiceField(queryset=Position.objects.all(), label=_('Position Name'))
    serial_number = forms.CharField(label=_('Component Serial No.'), max_length=50)
    status = forms.ChoiceField(label=_('Component Status'), choices=STATUS, 
    initial=GOOD)
    image = forms.ImageField(label=_('Image'), initial="default.jpeg", required=False)
    purchase_amount = forms.DecimalField(widget=forms.NumberInput, initial=0, max_digits=9, 
    decimal_places=2, label=_('Purchase Amount'))
    date_purchased = forms.DateTimeField(widget=forms.DateTimeInput, initial=timezone.now, 
    label=_('Date Purchased'))
    date_allocated = forms.DateTimeField(widget=forms.DateTimeInput, initial=timezone.now, label=_('Date Allocated'))
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
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label=_('Group'))
    system = forms.ModelChoiceField(queryset=System.objects.all(), label=_('System'))
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label=_('Type'))
    subtype = forms.ModelChoiceField(queryset=SubType.objects.all(), label=_('SubType'))
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)
	

    def __init__(self, *args, **kwargs):
        super(AllocationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "allocation-form-id"
        self.helper.form_class = "allocation-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Component Allocation'),)),
            BS5Accordion(
            AccordionGroup(_('ALLOCATE COMPONENT'),
                Row(
                Column('allocation_no', css_class='form-group col-md-6 mb-0'),
                Column(FieldWithButtons('component', StrictButton('',  css_class="btn fa fa-plus",
                data_bs_toggle="modal", data_bs_target="#component")), css_class='form-group col-md-6 mb-0')),

                Row(
                    FieldWithButtons('vendor', StrictButton('',  css_class="btn fa fa-plus",
                    data_bs_toggle="modal", data_bs_target="#staticBackdrop"), 
                    css_class='form-group col-md-6 mb-0'),
                    Column('serial_number', css_class='form-group col-md-6 mb-0'),
                ),
                Row(Column('image', css_class='form-group col-md-12 mb-0'),),
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
                        FieldWithButtons('group', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#group"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('system', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#system"), css_class='form-group col-md-6 mb-0'),
                    ),
                Row(
                        FieldWithButtons('type', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#type"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('subtype', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#subtype"), css_class='form-group col-md-6 mb-0'),

                    ),
            ),
            AccordionGroup(_('ATTACH TO LOCATION'),
                Row(
                        FieldWithButtons('company', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#company"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('division', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#division"), css_class='form-group col-md-6 mb-0'),
                    ),
                Row(
                        FieldWithButtons('branch', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#branch"), css_class='form-group col-md-6 mb-0'),
                        FieldWithButtons('position', StrictButton('',  css_class="btn fa fa-plus",
                        data_bs_toggle="modal", data_bs_target="#position"), css_class='form-group col-md-6 mb-0'),
                    ),   
            ),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            flush=True,
            always_open=True),
            Submit('save_componentallocation', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Allocation
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')


class VendorForm(forms.ModelForm):
    name = forms.CharField(label=_('Vendor Name'), 
    widget=forms.TextInput, max_length=100)
    address = forms.CharField(required=False, max_length=255)
    contacts = forms.CharField(required=False, max_length=255)
    manager = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length = 254, required=False)
    notes = forms.CharField(label=_('Notes'), widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = "vendor-form-id"
        self.helper.form_class = "vendor-form-class"
        self.helper.layout = Layout(
                HTML("""
            <p><strong style="float: center; font-size: 24px; margin-bottom: 0px;">{}</strong></p>
            <hr>
        """.format(_('Add New Vendor'),)),
            BS5Accordion(
            AccordionGroup(_('Vendor Data'),
            Row(Column('name', css_class='form-group col-md-12 mb-0'),),
            Row(Column('address', css_class='form-group col-md-12 mb-0'),),
            Row(Column('contacts', css_class='form-group col-md-12 mb-0'),),
            Row(Column('manager', css_class='form-group col-md-12 mb-0'),),
            Row(Column('email', css_class='form-group col-md-12 mb-0'),),
            Row(Column('notes', css_class='form-group col-md-12 mb-0'),),
            ),
             flush=True,
            always_open=True),
            Submit('save_vendor', _('Save and Close'), css_class='btn btn-primary fas fa-save'),
            Reset('reset', 'Clear', css_class='btn btn-danger'),
        )
    
    class Meta:
        model = Vendor
        exclude = ('date_created', 'date_modified', 'slug', 'created_by', 'modified_by')

