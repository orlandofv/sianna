import json
from multiprocessing import context
import pstats
import datetime
from decimal import Decimal

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
from .models import Component, MaintenanceSchedule, Allocation, Maintenance, Item, MaintenanceItem
from .filters import ComponentFilter
from users.models import User
from .forms import (ComponentForm, MaintenanceForm, MaintenanceScheduleForm, 
CompanyForm, DivisionForm, BranchForm, PositionForm, GroupForm, SystemForm, 
TypeForm, SubTypeForm, AllocationForm, VendorForm, ItemForm, MaintenanceFormModal,  
MaintenanceScheduleFormModal, ComponentUpdateForm)
from django.contrib import messages #import messages
from django.utils.translation import ugettext_lazy as _
from config.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers

from utilities.utilities import handle_uploaded_file


def home_view(request):
    context = {
        'components': Component.objects.all()
    }
    return render(request, 'index.html', context)


class ComponentListView(ListView):
    model = Component
    template_name = 'asset_app/listviews/component_list_view.html'


@login_required
def component_create_view(request):

    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        modal_form =  MaintenanceScheduleFormModal(request.POST)

        if form.is_valid() or modal_form.is_valid():
            try:
                if request.POST.get('save_schedule'):
                    instance = modal_form.save(commit=False)
                    instance.created_by =  instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    instance = instance.save()
                    return redirect('asset_app:component_create')
                else:
                    instance = form.save(commit=False)
                    instance.created_by =  instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    instance = instance.save()
                  
                    messages.success(request, _("Component added successfully!"))
                    if request.POST.get('save_component'):
                        return redirect('asset_app:component_list_view')
                    else:
                        return redirect('asset_app:component_create')
            except Exception as e:
                messages.error(request, e.args)
                return redirect('asset_app:component_create')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'asset_app/createviews/component_create.html', context)
    else:
        form = ComponentForm()
        modal_form =MaintenanceScheduleFormModal()
        context = {'form': form, 'modal_form': modal_form}
        return render(request, 'asset_app/createviews/component_create.html', context)


@login_required
def component_update_view(request, slug):
    
    # fetch the object related to passed id
    obj = get_object_or_404(Component, slug=slug)
 
    # pass the object as instance in form
    form = ComponentUpdateForm(request.POST or None, request.FILES or None, instance = obj)
    modal_form = MaintenanceScheduleFormModal(request.POST or None)
    
    if request.method == 'POST':
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid() or modal_form.is_valid():
            if request.POST.get('save_component'):
                
                instance = form.save(commit=False)
                _slug = slugify("{} - {}".format(instance.component_no, instance.name))
                instance.slug = _slug
                instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                messages.success(request, _("Data updated successfully!"))
                return redirect('asset_app:component_list_view')
            else:
                instance = modal_form.save(commit=False)
                instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                return redirect('asset_app:component_update_view', slug=slug)
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('asset_app:component_update_view', slug=slug)

    # dictionary for initial data with
    # field names as keys
    context ={}
    # add form dictionary to context
    context["form"] = form
    context["modal_form"] = modal_form
 
    return render(request, "asset_app/updateviews/component_update.html", context)


@login_required
def component_delete_view(request):

    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Component.objects.filter(id__in=selected_ids).delete()
        
        messages.success(request, _("Component(s) delete successfully!"))
        return redirect('asset_app:component_list_view')


# after updating it will redirect to detail_View
@login_required
def component_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    context ={}
  
    # add the dictionary during initialization
    context["data"] = Component.objects.get(slug=slug)
          
    return render(request, "asset_app/detailviews/component_detail_view.html", context)


########################## Maintenances ##########################

@login_required
def maintenance_create_view(request):
    
    # request should be ajax and method should be POST.
    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by =  instance.modified_by = request.user
            instance.date_created = instance.date_modified = datetime.datetime.now()
            instance = instance.save()
            
            if request.POST.get('save_maintenance'):
                messages.success(request, _("'{}' added successfully!".format(request.POST.get('name'))))
                return redirect('/')
            else:
                print(instance)
                return JsonResponse({"instance": instance}, status=200)
        
        else:
            if request.POST.get('save_maintenance'):
                for error in form.errors.values():
                    messages.error(request, error)
                return render(request, 'asset_app/createviews/maintenance_create.html', {'form': form})
            else:
                return JsonResponse({"error": form.errors.as_json()}, status=400) 
    else:
        # If request is not POST    
        form = MaintenanceForm()

        maintenance = Maintenance.objects.all()
        context = {'form': form, 'maintenance': maintenance}
        return render(request, 'asset_app/createviews/maintenance_create.html', context)

@login_required
def maintenance_update_view(request, slug):
    obj = get_object_or_404(Maintenance, slug=slug)

    if obj:
        if request.method == 'POST':
            form = MaintenanceForm(request.POST, instance=obj)

             # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save(commit=False)
                instance.created_by =  instance.modified_by = request.user
                instance.date_created = instance.date_modified = datetime.datetime.now()
                instance = instance.save()
                
                if request.POST.get('save_maintenance'):
                    messages.success(request, _("'{}' added successfully!".format(request.POST.get('name'))))
                    return redirect('/')
                else:
                    print(instance)
                    return JsonResponse({"instance": instance}, status=200)
            
            else:
                if request.POST.get('save_maintenance'):
                    for error in form.errors.values():
                        messages.error(request, error)
                    return render(request, 'asset_app/createviews/maintenance_create.html', {'form': form})
                else:
                    return JsonResponse({"error": form.errors.as_json()}, status=400) 
        else:
            # If request is not POST    
            form = MaintenanceForm()

            maintenance = Maintenance.objects.all()
            context = {'form': form, 'maintenance': maintenance}
            return render(request, 'asset_app/createviews/maintenance_create.html', context)
    else:
        # If request is not POST    
        form = MaintenanceForm()

        maintenance = Maintenance.objects.all()
        context = {'form': form, 'maintenance': maintenance}
        return render(request, 'asset_app/createviews/maintenance_create.html', context)

@login_required
def maintenance_delete_view(request):

    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Maintenance.objects.filter(id__in=selected_ids).delete()
        
        messages.success(request, _("Maintenance(s) delete successfully!"))
        return redirect('asset_app:maintenances_list_view')


@login_required
def maintenance_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    maintenance = get_object_or_404(Maintenance, slug=slug)
    items = MaintenanceItem.objects.filter(maintenance=maintenance)

    context ={}
    # add the dictionary during initialization
    context["data"] = Maintenance.objects.get(slug=slug)
    context["items"] = items
    
          
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


########################## Maintenance Schedule ##########################
@login_required
def maintenance_schedule_create_view(request):
    
    if request.method == 'POST':  
        form = MaintenanceScheduleForm(request.POST)
        maintenance_form = MaintenanceFormModal(request.POST)

        if form.is_valid() or maintenance_form.is_valid():
            try:
                if  request.POST.get('save_maintenance_modal'):
                    instance = maintenance_form.save(commit=False)
                    instance.created_by =  instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    instance = instance.save()
                    return redirect("asset_app:maintenance_schedule_create")
                else:
                    instance = form.save(commit=False)
                    instance.created_by =  instance.modified_by = request.user
                    instance.date_created = instance.date_modified = datetime.datetime.now()
                    instance = instance.save()
                    messages.success(request, _("Maintenance Schedule added successfully!"))
                    if request.POST.get('save_schedule'):
                        return redirect('asset_app:maintenance_schedule_list_view')
                    else:
                        return redirect("asset_app:maintenance_schedule_create")

            except Exception as e:
                messages.error(request, _("Error: {}".format(e.args)))
                return redirect('asset_app:maintenance_schedule_create')
        else:
            if request.POST.get('save_maintenance_modal'):
                messages.error(request, _('Maintenance form got errors. Data not saved!'))
            else:
                for error in form.errors.values():
                    messages.error(request, error)
            return redirect('asset_app:maintenance_schedule_create')

    else:        
        form = MaintenanceScheduleForm()
        maintenance_form = MaintenanceFormModal()
        context = {'form': form, 'modal_form': maintenance_form}
        return render(request, 'asset_app/createviews/maintenance_schedule_create.html', context)


@login_required
def maintenance_schedule_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    maintenance = get_object_or_404(MaintenanceSchedule, slug=slug)
    items = Maintenance.objects.filter(maintenance=maintenance)

    context ={}
    # add the dictionary during initialization
    context["data"] = maintenance
    context["items"] = items
    
          
    return render(request, "asset_app/detailviews/maintenance_schedule_detail_view.html", context)


@login_required
def maintenance_schedule_delete_view(request):

    print(request.method)
    
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                MaintenanceSchedule.objects.filter(id__in=selected_ids).delete()
        
        messages.success(request, _("Maintenance Schedule(s) delete successfully!"))
        return redirect('asset_app:maintenance_schedule_list_view')


def company_create_view(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Company added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = CompanyForm()
    context = {'form': form}
    return render(request, 'asset_app/createviews/company_create.html', context)


def division_create_view(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        modal_form = CompanyForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Division added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = DivisionForm()
    modal_form = CompanyForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/division_create.html', context)


def branch_create_view(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        modal_form = DivisionForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Branch added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = BranchForm()
    modal_form = DivisionForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/branch_create.html', context)


def position_create_view(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        modal_form = BranchForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Position added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = PositionForm()
    modal_form = BranchForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/position_create.html', context)


def group_create_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = GroupForm()
    context = {'form': form}
    return render(request, 'asset_app/createviews/group_create.html', context)


def system_create_view(request):
    if request.method == 'POST':
        form = SystemForm(request.POST)
        modal_form = GroupForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("System added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))
            
    form = SystemForm()
    modal_form = GroupForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/system_create.html', context)


def type_create_view(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        modal_form = SystemForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Type added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = TypeForm()
    modal_form = SystemForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/type_create.html', context)


def subtype_create_view(request):
    if request.method == 'POST':
        form = SubTypeForm(request.POST)
        modal_form = TypeForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("SubType added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = SubTypeForm()
    modal_form = TypeForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/subtype_create.html', context)


def vendor_create_view(request):
    if request.method == 'POST' and 'save_vendor':
        form = VendorForm(request.POST)
       
        if form.is_valid() and 'save_vendor':
            form.save()
            messages.success(request, _("Vendor added successfully!"))
            return redirect('/')
      
    form = VendorForm()
    context = {'form': form,}
    return render(request, 'asset_app/createviews/vendor_create.html', context)


class AllocationListView(ListView):
    model = Allocation
    template_name = 'asset_app/listviews/allocation_list_view.html'


def allocation_create_view(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        component_form = ComponentForm(request.POST)
        vendor_form = VendorForm(request.POST)
        group_form = GroupForm(request.POST)
        system_form = SystemForm(request.POST)
        type_form = TypeForm(request.POST)
        subtype_form = SubTypeForm(request.POST)
        company_form = CompanyForm(request.POST)
        division_form = DivisionForm(request.POST)
        branch_form = BranchForm(request.POST)
        position_form = PositionForm(request.POST)

        if vendor_form.is_valid() and 'save_vendor':
            vendor_form.save()
           
        if component_form.is_valid() and 'save_component':
            component_form.save()
           
        if group_form.is_valid() and 'save_group':
            group_form.save()
            
        if system_form.is_valid() and 'save_system':
            system_form.save()
          
        if type_form.is_valid() and 'save_type':
            type_form.save()
           
        if subtype_form.is_valid() and 'save_subtype':
            subtype_form.save()
            
        if company_form.is_valid() and 'save_company':
            company_form.save()
        
        if division_form.is_valid() and 'save_division':
            division_form.save()
           
        if branch_form.is_valid() and 'save_branch':
            branch_form.save()
        
        if position_form.is_valid() and 'save_position':
            position_form.save()
       
        if form.is_valid() and 'save_componentallocation':
            try:
                form.save()
                messages.success(request, _("Component Allocation added successfully!"))
                return redirect('asset_app:')
            except Exception as e:
                messages.error(request, list(form.errors))
       
    form = AllocationForm()
    component_form = ComponentForm()
    vendor_form = VendorForm()
    group_form = GroupForm()
    system_form = SystemForm()
    type_form = TypeForm()
    subtype_form = SubTypeForm()
    company_form = CompanyForm()
    division_form = DivisionForm()
    branch_form = BranchForm()
    position_form = PositionForm()
    context = {'form': form, 'vendor_form': vendor_form, "group_form": group_form,
    "system_form": system_form, "type_form": type_form, "subtype_form": subtype_form,
    "company_form": company_form, "division_form": division_form, "branch_form": branch_form ,
    "position_form": position_form, 'component_form': component_form}
    return render(request, 'asset_app/createviews/allocation_create.html', context)

###################### ************ LIST VIEWS ************  ######################
class MaintenanceScheduleListView(ListView):
    model = MaintenanceSchedule
    template_name = 'asset_app/listviews/maintenance_schedule_list_view.html'


class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'asset_app/listviews/maintenance_list_view.html'


def item_delete_view(request):
    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                MaintenanceItem.objects.filter(id__in=selected_ids).delete()

        return redirect('asset_app:component_list_view')



