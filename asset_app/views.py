import json
from multiprocessing import context
import pstats
import datetime
from decimal import Decimal
import os

from django.db import connection
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
from .models import (Component, Allocation, Maintenance, Item, 
MaintenanceItem, Company, Division, Branch, Position, Group, System, Type, 
SubType, Vendor, Settings, WorkOrder, Action)
from .filters import ComponentFilter
from users.models import User
from .forms import (ComponentForm, MaintenanceForm, CompanyForm, DivisionForm, BranchForm, 
PositionForm, GroupForm, SystemForm, TypeForm, SubTypeForm, AllocationForm, 
VendorForm, ItemForm, SettingsForm, WorkOrderForm)
from django.contrib import messages #import messages
from django.utils.translation import ugettext_lazy as _
from config.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings


import qrcode

from utilities.utilities import handle_uploaded_file


########################## Settings ##########################
@login_required
def settings_create_view(request):
    obj = Settings.objects.first()
    form = SettingsForm(request.POST or None, request.FILES or None, instance=obj)

    if request.method == 'POST':
       
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Settings added successfully!"))

            if request.POST.get('save_settings'):
                return redirect('asset_app:home')
            else:
                return redirect('asset_app:settings_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:settings_create')
    
    context = {'form': form}
    return render(request, 'asset_app/createviews/settings_create.html', context)


@login_required
def home_view(request):
    context = {
        'component': Component.objects.all(), 
        'maitntenance': Maintenance.objects.all(), 
        'company': Company.objects.all(), 
        'division': Division.objects.all(), 
        'branch': Branch.objects.all(), 
        'position': Position.objects.all(), 
        'allocation': Allocation.objects.all(), 
        'group': Group.objects.all(), 
        'system': System.objects.all(), 
        'type': Type.objects.all(), 
        'subtype': SubType.objects.all(), 
        'vendor': Vendor.objects.all(), 
        'item': Item.objects.all(), 
        'settings': Settings.objects.all(),
    }
    return render(request, 'index.html', context)


########################## Maintenance ##########################
class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'asset_app/listviews/maintenance_list_view.html'


@login_required
def maintenance_create_view(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            maintenance = instance

            instance = instance.save()
            
            # Saves actions
            save_action(request, maintenance)

            messages.success(request, _("Maintenance added successfully!"))

            if request.POST.get('save_maintenance'):
                return redirect('asset_app:maintenances_list')
            else:
                return redirect('asset_app:maintenance_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:maintenance_create')
    else:
        form = MaintenanceForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/maintenance_create.html', context)


def save_action(request, instance):

    post = dict(request.POST)
    actions = post['action']
    costs = post['cost']

    i = 0
    for c in actions:
        try:
            action_object = Action(name=c, maintenance=instance, slug=slugify(c), cost=costs[i], 
            date_created=datetime.datetime.now(), date_modified=datetime.datetime.now(), 
            created_by=request.user, modified_by=request.user)

            action_object.save()

        except Exception as e:
            print(e)
            return e
        i += 1

    return action_object


@login_required
def maintenance_update_view(request, slug):
    maintenance = get_object_or_404(Maintenance, slug=slug)
    form = MaintenanceForm(request.POST or None, instance=maintenance)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Maintenance apdated successfully!"))

            if request.POST.get('save_maintenance'):
                return redirect('asset_app:maintenances_list')
            else:
                return redirect('asset_app:maintenance_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:maintenance_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/maintenance_update.html', context)


@login_required
def maintenance_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Maintenance.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Maintenance delete successfully!"))
        return redirect('asset_app:maintenances_list')


def maintenance_dashboard_view(request):
    ROUTINE = 'Routine'
    PREVENTIVE = 'Preventive'
    CORRECTIVE = 'Corrective'
    PREDECTIVE = 'Predective'

    last_maintenances =  Maintenance.objects.all().order_by('-date_created')[:15]
    total_maintenances =  Maintenance.objects.all().count()
    all_maintenances = Maintenance.objects.all().order_by('name')
    preventive_maintenances = Allocation.component.maintenance.objects.filter(type=PREVENTIVE).count()
    routine_maintenances = Maintenance.objects.filter(type=ROUTINE).count()
    corrective_maintenances = Maintenance.objects.filter(type=CORRECTIVE).count()
    predective_maintenances = Maintenance.objects.filter(type=PREDECTIVE).count()
    
    context = {}
    context['total'] = total_maintenances
    context['last'] = last_maintenances
    context['all'] = all_maintenances
    context['preventive'] = preventive_maintenances
    context['routine'] = routine_maintenances
    context['corrective'] = corrective_maintenances
    context['predective'] = predective_maintenances

    return render(request, 'asset_app/dashboardviews/maintenance_dashboard.html', context=context)


@login_required
def maintenance_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    maintenance = get_object_or_404(Maintenance, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = maintenance    
    return render(request, "asset_app/detailviews/maintenance_detail_view.html", context)


@login_required
def maintenance_item_create_view(request, slug):

    maintenance = get_object_or_404(Maintenance, slug=slug)
    items = MaintenanceItem.objects.filter(maintenance=maintenance)

    if request.method == 'POST':
        form = ItemForm(request.POST)

        # Get the object from the form
        obj = request.POST.get('name')
        
        try:
            item_object = Item.objects.get(name=obj)
        except Exception as e:
            print(e)
            item_object = None

        quantity = Decimal(request.POST.get('quantity'))

        # save the data and after fetch the object in instance
        if item_object:
            item = Item.objects.get(name=obj)
            try:
                instance = MaintenanceItem(maintenance=maintenance, item=item, quantity=quantity) 
                instance.save()

            except Exception as e:
                print(e)
                messages.error(request, _('Item with this name already exists'))
                return render(request, 'asset_app/createviews/item_create.html', 
                {'maintenance': maintenance, 'form': form, 'items': items})
        else:
            item = Item()
            item.name = obj
            item.quantity = Decimal(request.POST.get('quantity'))
            item.created_by =  item.modified_by = request.user
            item.date_created = item.date_modified = datetime.datetime.now()

            try:
                item.save()
                m =  MaintenanceItem(maintenance=maintenance, item=item, quantity=quantity)
                m.save()
            except Exception as e:
                print(e)
                messages.error(request, _('Item with this name already exists'))
                return render(request, 'asset_app/createviews/item_create.html', 
                {'maintenance': maintenance, 'form': form, 'items': items})

        messages.success(request, _("'{}' added successfully!".format(item.name)))
        return redirect('asset_app:item_create', slug=slug)
    else:
        form = ItemForm(None)
        return render(request, 'asset_app/createviews/item_create.html', 
        {'maintenance': maintenance, 'form': form, 'items': items})

@login_required
def maintenance_item_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                MaintenanceItem.objects.filter(id__in=selected_ids).delete()

        return redirect('asset_app:components_list')


########################## Component ##########################
class ComponentListView(LoginRequiredMixin, ListView):
    model = Component
    template_name = 'asset_app/listviews/component_list_view.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        components = Component.objects.all()

        c = {}
        for x in components:
            c['component_no'] = x.component_no 
            c['name'] = x.name 
            c['slug'] = x.slug 
            c['manufacturer'] = x.manufacturer 
            c['stock_code'] = x.stock_code 
            c['maintenance'] = x.maintenance 
            c['image'] = x.image  
            c['notes'] = x.notes  
            c['date_created'] = x.date_created  
            c['date_modified'] = x.date_modified  
            c['created_by'] = x.created_by 
            c['modified_by'] = x.modified_by  

        context['allocation'] = Allocation.objects.all()
        context['data'] = c
        return context


@login_required
def component_create_view(request):
    if request.method == 'POST':
        form = ComponentForm(request.POST)
        maintenance_form = MaintenanceForm(request.POST)

        if form.is_valid() or maintenance_form.is_valid():
            if request.POST.get('save_maintenance') or request.POST.get('save_maintenance_new'):
                instance = maintenance_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:component_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Component added successfully!"))

                if request.POST.get('save_component'):
                    return redirect('asset_app:components_list')
                else:
                    return redirect('asset_app:component_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:component_create')
    else:
        form = ComponentForm()
        maintenance_form = MaintenanceForm()
        context = {'form': form, 'maintenance_form': maintenance_form}
        return render(request, 'asset_app/createviews/component_create.html', context)


@login_required
def component_dashboard_view(request):
    
    GOOD = 'Good'
    BROKEN = 'Broken'
    
    last_components =  Component.objects.all().order_by('-date_created')[:15]
    total_components =  Component.objects.all().count()
    all_components = Component.objects.all().order_by('name')
    broken_components = Allocation.objects.filter(status=BROKEN).count()
    good_components = Allocation.objects.filter(status=GOOD).count()

    cursor = connection.cursor()
    print(cursor)
    cursor.execute("""SELECT DISTINCT component_id FROM asset_app_allocation
    GROUP BY component_id""")
    data = cursor.fetchall()
    allocated_components = len(data)
    
    context = {}
    context['total'] = total_components
    context['last'] = last_components
    context['all'] = all_components
    context['broken'] = broken_components
    context['good'] = good_components
    context['allocated'] = allocated_components
    context['not_allocated'] = total_components - allocated_components
   
    return render(request, 'asset_app/dashboardviews/component_dashboard.html', context=context)


@login_required
def component_update_view(request, slug):
    component = get_object_or_404(Component, slug=slug)
    form = ComponentForm(request.POST or None, instance=component)
    maintenance_form = MaintenanceForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Component apdated successfully!"))

            if request.POST.get('save_component'):
                return redirect('asset_app:components_list')
            else:
                return redirect('asset_app:component_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:component_update', slug=slug)
       
    context = {'form': form, 'maintenance_form': maintenance_form}
    return render(request, 'asset_app/updateviews/component_update.html', context)


@login_required
def component_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Component.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Component delete successfully!"))
        return redirect('asset_app:components_list')


@login_required
def component_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    component = get_object_or_404(Component, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = component    
    return render(request, "asset_app/detailviews/component_detail_view.html", context)


########################## Company ##########################
class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'asset_app/listviews/company_list_view.html'


@login_required
def company_create_view(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
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
            messages.success(request, _("Company added successfully!"))

            if request.POST.get('save_company'):
                return redirect('asset_app:companies_list')
            else:
                return redirect('asset_app:company_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:company_create')
    else:
        form = CompanyForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/company_create.html', context)


@login_required
def company_update_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    form = CompanyForm(request.POST or None, instance=company)

    if request.method == 'POST':
    
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Company apdated successfully!"))

            if request.POST.get('save_company'):
                return redirect('asset_app:companies_list')
            else:
                return redirect('asset_app:company_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:company_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/company_update.html', context)


@login_required
def company_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Company.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Company delete successfully!"))
        return redirect('asset_app:companies_list')


@login_required
def company_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    company = get_object_or_404(Company, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = company    
    return render(request, "asset_app/detailviews/company_detail_view.html", context)


########################## Division ##########################
class DivisionListView(LoginRequiredMixin, ListView):
    model = Division
    template_name = 'asset_app/listviews/division_list_view.html'


@login_required
def division_create_view(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        company_form = CompanyForm(request.POST)

        if form.is_valid() or company_form.is_valid():
            if request.POST.get('save_company') or request.POST.get('save_company_new'):
                instance = company_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:division_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Division added successfully!"))

                if request.POST.get('save_division'):
                    return redirect('asset_app:divisions_list')
                else:
                    return redirect('asset_app:division_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:division_create')
    else:
        form = DivisionForm()
        company_form = CompanyForm()
        context = {'form': form, 'company_form': company_form}
        return render(request, 'asset_app/createviews/division_create.html', context)


@login_required
def division_update_view(request, slug):
    division = get_object_or_404(Division, slug=slug)
    form = DivisionForm(request.POST or None, instance=division)
    company_form = CompanyForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Division apdated successfully!"))

            if request.POST.get('save_division'):
                return redirect('asset_app:divisions_list')
            else:
                return redirect('asset_app:division_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:division_update', slug=slug)
       
    context = {'form': form, 'company_form': company_form}
    return render(request, 'asset_app/updateviews/division_update.html', context)


@login_required
def division_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Division.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Division delete successfully!"))
        return redirect('asset_app:divisions_list')


@login_required
def division_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    division = get_object_or_404(Division, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = division    
    return render(request, "asset_app/detailviews/division_detail_view.html", context)


########################## Branch ##########################
class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    template_name = 'asset_app/listviews/branch_list_view.html'


@login_required
def branch_create_view(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        division_form = DivisionForm(request.POST)

        if form.is_valid() or division_form.is_valid():
            if request.POST.get('save_division') or request.POST.get('save_division_new'):
                instance = division_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:branch_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Branch added successfully!"))

                if request.POST.get('save_branch'):
                    return redirect('asset_app:branches_list')
                else:
                    return redirect('asset_app:branch_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:branch_create')
    else:
        form = BranchForm()
        division_form = DivisionForm()
        context = {'form': form, 'division_form': division_form}
        return render(request, 'asset_app/createviews/branch_create.html', context)


@login_required
def branch_update_view(request, slug):
    branch = get_object_or_404(Branch, slug=slug)
    form = BranchForm(request.POST or None, instance=branch)
    division_form = DivisionForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Branch apdated successfully!"))

            if request.POST.get('save_branch'):
                return redirect('asset_app:branches_list')
            else:
                return redirect('asset_app:branch_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:branch_update', slug=slug)
       
    context = {'form': form, 'division_form': division_form}
    return render(request, 'asset_app/updateviews/branch_update.html', context)


@login_required
def branch_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Branch.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Branch delete successfully!"))
        return redirect('asset_app:branches_list')


@login_required
def branch_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    branch = get_object_or_404(Branch, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = branch    
    return render(request, "asset_app/detailviews/branch_detail_view.html", context)


########################## Position ##########################
class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = 'asset_app/listviews/position_list_view.html'


@login_required
def position_create_view(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        branch_form = BranchForm(request.POST)

        if form.is_valid() or branch_form.is_valid():
            if request.POST.get('save_branch') or request.POST.get('save_branch_new'):
                instance = branch_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:position_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Position added successfully!"))

                if request.POST.get('save_position'):
                    return redirect('asset_app:positions_list')
                else:
                    return redirect('asset_app:position_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:position_create')
    else:
        form = PositionForm()
        branch_form = BranchForm()
        context = {'form': form, 'branch_form': branch_form}
        return render(request, 'asset_app/createviews/position_create.html', context)


@login_required
def position_update_view(request, slug):
    position = get_object_or_404(Position, slug=slug)
    form = PositionForm(request.POST or None, instance=position)
    branch_form = BranchForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Position apdated successfully!"))

            if request.POST.get('save_position'):
                return redirect('asset_app:positions_list')
            else:
                return redirect('asset_app:position_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:position_update', slug=slug)
       
    context = {'form': form, 'branch_form': branch_form}
    return render(request, 'asset_app/updateviews/position_update.html', context)


@login_required
def position_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Position.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Position delete successfully!"))
        return redirect('asset_app:positions_list')


@login_required
def position_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    position = get_object_or_404(Position, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = position    
    return render(request, "asset_app/detailviews/position_detail_view.html", context)


########################## Group ##########################
class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'asset_app/listviews/group_list_view.html'


@login_required
def group_create_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Group added successfully!"))

            if request.POST.get('save_group'):
                return redirect('asset_app:groups_list')
            else:
                return redirect('asset_app:group_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:group_create')
    else:
        form = GroupForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/group_create.html', context)


@login_required
def group_update_view(request, slug):
    group = get_object_or_404(Group, slug=slug)
    form = GroupForm(request.POST or None, instance=group)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Group apdated successfully!"))

            if request.POST.get('save_group'):
                return redirect('asset_app:groups_list')
            else:
                return redirect('asset_app:group_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:group_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/group_update.html', context)


@login_required
def group_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Group.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Group delete successfully!"))
        return redirect('asset_app:groups_list')


@login_required
def group_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    group = get_object_or_404(Group, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = group    
    return render(request, "asset_app/detailviews/group_detail_view.html", context)


########################## System ##########################
class SystemListView(LoginRequiredMixin, ListView):
    model = System
    template_name = 'asset_app/listviews/system_list_view.html'


@login_required
def system_create_view(request):
    if request.method == 'POST':
        form = SystemForm(request.POST)
        group_form = GroupForm(request.POST)

        if form.is_valid() or group_form.is_valid():
            if request.POST.get('save_group') or request.POST.get('save_group_new'):
                instance = group_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:system_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("System added successfully!"))

                if request.POST.get('save_system'):
                    return redirect('asset_app:systems_list')
                else:
                    return redirect('asset_app:system_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:system_create')
    else:
        form = SystemForm()
        group_form = GroupForm()
        context = {'form': form, 'group_form': group_form}
        return render(request, 'asset_app/createviews/system_create.html', context)


@login_required
def system_update_view(request, slug):
    system = get_object_or_404(System, slug=slug)
    form = SystemForm(request.POST or None, instance=system)
    group_form = GroupForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("System apdated successfully!"))

            if request.POST.get('save_system'):
                return redirect('asset_app:systems_list')
            else:
                return redirect('asset_app:system_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:system_update', slug=slug)
       
    context = {'form': form, 'group_form': group_form}
    return render(request, 'asset_app/updateviews/system_update.html', context)


@login_required
def system_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                System.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("System delete successfully!"))
        return redirect('asset_app:systems_list')


@login_required
def system_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    system = get_object_or_404(System, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = system    
    return render(request, "asset_app/detailviews/system_detail_view.html", context)


########################## Type ##########################
class TypeListView(LoginRequiredMixin, ListView):
    model = Type
    template_name = 'asset_app/listviews/type_list_view.html'


def type_create_view(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        system_form = SystemForm(request.POST)

        if form.is_valid() or system_form.is_valid():
            if request.POST.get('save_system') or request.POST.get('save_system_new'):
                instance = system_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:type_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Type added successfully!"))

                if request.POST.get('save_type'):
                    return redirect('asset_app:types_list')
                else:
                    return redirect('asset_app:type_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:type_create')
    else:
        form = TypeForm()
        system_form = SystemForm()
        context = {'form': form, 'system_form': system_form}
        return render(request, 'asset_app/createviews/type_create.html', context)


@login_required
def type_update_view(request, slug):
    type = get_object_or_404(Type, slug=slug)
    form = TypeForm(request.POST or None, instance=type)
    system_form = SystemForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Type apdated successfully!"))

            if request.POST.get('save_type'):
                return redirect('asset_app:types_list')
            else:
                return redirect('asset_app:type_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:type_update', slug=slug)
       
    context = {'form': form, 'system_form': system_form}
    return render(request, 'asset_app/updateviews/type_update.html', context)


@login_required
def type_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Type.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Type delete successfully!"))
        return redirect('asset_app:types_list')


@login_required
def type_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    type = get_object_or_404(Type, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = type    
    return render(request, "asset_app/detailviews/type_detail_view.html", context)


########################## SubType ##########################
class SubTypeListView(LoginRequiredMixin, ListView):
    model = SubType
    template_name = 'asset_app/listviews/subtype_list_view.html'


@login_required
def subtype_create_view(request):
    if request.method == 'POST':
        form = SubTypeForm(request.POST)
        type_form = TypeForm(request.POST)

        if form.is_valid() or type_form.is_valid():
            if request.POST.get('save_type') or request.POST.get('save_type_new'):
                instance = type_form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:subtype_create')
            else:
                instance = form.save(commit=False)
                instance.created_by = instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("SubType added successfully!"))

                if request.POST.get('save_subtype'):
                    return redirect('asset_app:subtypes_list')
                else:
                    return redirect('asset_app:subtype_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:subtype_create')
    else:
        form = SubTypeForm()
        type_form = TypeForm()
        context = {'form': form, 'type_form': type_form}
        return render(request, 'asset_app/createviews/subtype_create.html', context)


@login_required
def subtype_update_view(request, slug):
    subtype = get_object_or_404(SubType, slug=slug)
    form = SubTypeForm(request.POST or None, instance=subtype)
    type_form = TypeForm(request.POST or None)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("SubType apdated successfully!"))

            if request.POST.get('save_subtype'):
                return redirect('asset_app:subtypes_list')
            else:
                return redirect('asset_app:subtype_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:subtype_update', slug=slug)
       
    context = {'form': form, 'type_form': type_form}
    return render(request, 'asset_app/updateviews/subtype_update.html', context)


@login_required
def subtype_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                SubType.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("SubType delete successfully!"))
        return redirect('asset_app:subtypes_list')


@login_required
def subtype_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    subtype = get_object_or_404(SubType, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = subtype    
    return render(request, "asset_app/detailviews/subtype_detail_view.html", context)


########################## Vendor ##########################
class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'asset_app/listviews/vendor_list_view.html'


@login_required
def vendor_create_view(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Vendor added successfully!"))

            if request.POST.get('save_vendor'):
                return redirect('asset_app:vendors_list')
            else:
                return redirect('asset_app:vendor_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:vendor_create')
    else:
        form = VendorForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/vendor_create.html', context)


@login_required
def vendor_update_view(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    form = VendorForm(request.POST or None, instance=vendor)

    if request.method == 'POST':
        

        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.slug = slugify(instance.name)
            instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("Vendor apdated successfully!"))

            if request.POST.get('save_vendor'):
                return redirect('asset_app:vendors_list')
            else:
                return redirect('asset_app:vendor_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:vendor_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/vendor_update.html', context)


@login_required
def vendor_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Vendor.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Vendor delete successfully!"))
        return redirect('asset_app:vendors_list')


@login_required
def vendor_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    vendor = get_object_or_404(Vendor, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = vendor    
    return render(request, "asset_app/detailviews/vendor_detail_view.html", context)


########################## Allocation ##########################
class AllocationListView(LoginRequiredMixin, ListView):
    model = Allocation
    template_name = 'asset_app/listviews/allocation_list_view.html'


@login_required
def allocation_create_view(request):

    if request.method == 'POST':
        form = AllocationForm(request.POST, request.FILES)
        component_form = ComponentForm(request.POST)
        company_form = CompanyForm(request.POST)
        division_form = DivisionForm(request.POST)
        branch_form = BranchForm(request.POST)
        position_form = PositionForm(request.POST)
        group_form = GroupForm(request.POST)
        system_form = SystemForm(request.POST)
        type_form = TypeForm(request.POST)
        subtype_form = SubTypeForm(request.POST)
        vendor_form = VendorForm(request.POST)

        if form.is_valid() or company_form.is_valid() or component_form.is_valid() \
            or division_form.is_valid() or branch_form.is_valid() or position_form.is_valid() \
                or group_form.is_valid() or system_form.is_valid() or type_form.is_valid() \
                    or subtype_form.is_valid() or vendor_form.is_valid():

            if request.POST.get('save_component') or request.POST.get('save_component_new'):
                instance = component_form.save(commit=False)
            
            if request.POST.get('save_company') or request.POST.get('save_company_new'):
                instance = company_form.save(commit=False)
            
            if request.POST.get('save_division') or request.POST.get('save_division_new'):
                instance = division_form.save(commit=False)
            
            if request.POST.get('save_branch') or request.POST.get('save_branch_new'):
                instance = branch_form.save(commit=False)
            
            if request.POST.get('save_position') or request.POST.get('save_position_new'):
                instance = position_form.save(commit=False)
            
            if request.POST.get('save_group') or request.POST.get('save_group_new'):
                instance = group_form.save(commit=False)
            
            if request.POST.get('save_system') or request.POST.get('save_system_new'):
                instance = system_form.save(commit=False)
            
            if request.POST.get('save_type') or request.POST.get('save_type_new'):
                instance = type_form.save(commit=False)
            
            if request.POST.get('save_subtype') or request.POST.get('save_subtype_new'):
                instance = subtype_form.save(commit=False)
            
            if request.POST.get('save_vendor') or request.POST.get('save_vendor_new'):
                instance = vendor_form.save(commit=False)
            
            if request.POST.get('save_allocation') or request.POST.get('save_allocation_new'):
                instance = form.save(commit=False)

                try:
                    qrcode = create_qrcode(request, instance)
                    instance.qrcode = qrcode
                except Exception as e:
                    print(f'Error: {e}')

            
                messages.success(request, _("Allocation created successfully!"))

            instance.created_by = instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
    
            if request.POST.get('save_allocation'):
                return redirect('asset_app:allocations_list')
            else:
                return redirect('asset_app:allocation_create')

        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:allocation_create')
    else:
        form = AllocationForm()
        component_form = ComponentForm()
        company_form = CompanyForm()
        division_form = DivisionForm()
        branch_form = BranchForm()
        position_form = PositionForm()
        group_form = GroupForm()
        system_form = SystemForm()
        type_form = TypeForm()
        subtype_form = SubTypeForm()
        vendor_form = VendorForm()

        context = {'form': form, 'component_form': component_form,'company_form': company_form, 
        'division_form': division_form, 'branch_form': branch_form, 'position_form': position_form, 
        'group_form': group_form, 'system_form': system_form, 'type_form': type_form, 
        'subtype_form': subtype_form, 'vendor_form': vendor_form}
        return render(request, 'asset_app/createviews/allocation_create.html', context)


@login_required
def allocation_update_view(request, slug):
    allocation = get_object_or_404(Allocation, slug=slug)
    form = AllocationForm(request.POST or None, request.FILES or None, instance=allocation)
    component_form = ComponentForm(request.POST or None)
    company_form = CompanyForm(request.POST or None)
    division_form = DivisionForm(request.POST or None)
    branch_form = BranchForm(request.POST or None)
    position_form = PositionForm(request.POST or None)
    group_form = GroupForm(request.POST or None)
    system_form = SystemForm(request.POST or None)
    type_form = TypeForm(request.POST or None)
    subtype_form = SubTypeForm(request.POST or None)
    vendor_form = VendorForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid() or company_form.is_valid() or component_form.is_valid() \
                or division_form.is_valid() or branch_form.is_valid() or position_form.is_valid() \
                    or group_form.is_valid() or system_form.is_valid() or type_form.is_valid() \
                        or subtype_form.is_valid() or vendor_form.is_valid():
 
                if request.POST.get('save_component') or request.POST.get('save_component_new'):
                    instance = component_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_company') or request.POST.get('save_company_new'):
                    instance = company_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_division') or request.POST.get('save_division_new'):
                    instance = division_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_branch') or request.POST.get('save_branch_new'):
                    instance = branch_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_position') or request.POST.get('save_position_new'):
                    instance = position_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_group') or request.POST.get('save_group_new'):
                    instance = group_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_system') or request.POST.get('save_system_new'):
                    instance = system_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_type') or request.POST.get('save_type_new'):
                    instance = type_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_subtype') or request.POST.get('save_subtype_new'):
                    instance = subtype_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_vendor') or request.POST.get('save_vendor_new'):
                    instance = vendor_form.save(commit=False)
                    instance.created_by = instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                
                if request.POST.get('save_allocation') or request.POST.get('save_allocation_new'):
                    instance = form.save(commit=False)
                    instance.modified_by = request.user
                    instance.slug = slugify('{} - {}'.format(instance.allocation_no, instance.component))
                    instance.date_modified = datetime.datetime.now()
                    
                    try:
                        qrcode = create_qrcode(request, instance)
                        instance.qrcode = qrcode
                    except Exception as e:
                        print(f'Error: {e}')
            
                    messages.success(request, _("Allocation created successfully!"))

                instance = instance.save()
                    
                if request.POST.get('save_allocation'):
                    return redirect('asset_app:allocations_list')
                else:
                    return redirect('asset_app:allocation_update', slug=slug)
            else:
                for error in form.errors.values():
                    messages.error(request, error)
                return redirect('asset_app:allocation_update', slug=slug)

        except Exception as e:
            messages.error(request, e)
            return redirect('asset_app:allocation_update', slug=slug)
    
    context = {'form': form, 'component_form': component_form,'company_form': company_form, 
        'division_form': division_form, 'branch_form': branch_form, 'position_form': position_form, 
        'group_form': group_form, 'system_form': system_form, 'type_form': type_form, 
        'subtype_form': subtype_form, 'vendor_form': vendor_form}
    return render(request, 'asset_app/updateviews/allocation_update.html', context)


@login_required
def allocation_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Allocation.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("Allocation delete successfully!"))
        return redirect('asset_app:allocations_list')


@login_required
def allocation_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    allocation = get_object_or_404(Allocation, slug=slug)
   
    context ={}
    # add the dictionary during initialization
    context["data"] = allocation    
    return render(request, "asset_app/detailviews/allocation_detail_view.html", context)


########################## WorkOrder ##########################
class WorkOrderListView(LoginRequiredMixin, ListView):
    model = WorkOrder
    template_name = 'asset_app/listviews/workorder_list_view.html'


@login_required
def workorder_create_view(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            validate_workorder(request, instance)
            instance = instance.save()
            messages.success(request, _("WorkOrder added successfully!"))

            if request.POST.get('save_workorder'):
                return redirect('asset_app:workorders_list')
            else:
                return redirect('asset_app:workorder_create')
        else:
            print(form.errors)
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:workorder_create')
    else:
        form = WorkOrderForm()
        context = {'form': form}
        return render(request, 'asset_app/createviews/workorder_create.html', context)


@login_required
def workorder_update_view(request, slug):
    workorder = get_object_or_404(WorkOrder, slug=slug)
    form = WorkOrderForm(request.POST or None, instance=workorder)
   
    if request.method == 'POST':
    
        if form.is_valid():
            instance = form.save(commit=False)
            validate_workorder(request, instance)
            instance = instance.save()
            messages.success(request, _("WorkOrder apdated successfully!"))

            if request.POST.get('save_workorder'):
                return redirect('asset_app:workorders_list')
            else:
                return redirect('asset_app:workorder_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:workorder_update', slug=slug)
       
    context = {'form': form}
    return render(request, 'asset_app/updateviews/workorder_update.html', context)

def validate_workorder(request, instance):
    instance.modified_by = request.user
    instance.slug = instance.order
    instance.date_modified = datetime.datetime.now()

@login_required
def workorder_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                WorkOrder.objects.filter(id__in=selected_ids).delete()
        
        messages.warning(request, _("WorkOrder delete successfully!"))
        return redirect('asset_app:workorders_list')


@login_required
def workorder_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    workorder = get_object_or_404(WorkOrder, slug=slug)
   
    context = {}
    ramaining_time = workorder.end - datetime.datetime.now()
    # add the dictionary during initialization

    if workorder.end < datetime.datetime.now() and workorder.status in ('Pending', 'InProgress'):
        overdue = True
    else:
        overdue = False

    context["data"] = workorder    
    context["overdue"] = overdue    
    context["ramaining_time"] = ramaining_time    
    return render(request, "asset_app/detailviews/workorder_detail_view.html", context)


def create_qrcode(request, instance):
    media = settings.MEDIA_ROOT

    settings_model = Settings.objects.first()
    email = settings_model.email 
    
    allocation_no = instance.allocation_no
    component = instance.component
    company = instance.company 
    division = instance.division 
    branch = instance.branch 
    position = instance.position

    subject = _(f"There is a issue with {component}")
    body = f"""
    Allocation Number.: {allocation_no}\n
    Company: {company}\n
    Division: {division}\n
    Branch: {branch}\n
    Position: {position}\n

    We have identified a problem with this component: {allocation_no} - {component}
    """

    print(body)

    _file = f"{instance.slug}" + ".png"
    file = os.path.join(media, _file)

    # Absolute path of the file
    path = os.path.realpath(file)
    
    if os.path.exists(path):
        print('Exists')
    else:
        data = f"mailto: {email}?&subject={subject}&body={body}"
        img = qrcode.make(data)
        img.save(path)

    return _file

