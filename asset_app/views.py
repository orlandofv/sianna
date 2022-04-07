import json
from multiprocessing import context
import pstats
import datetime

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
from .models import Component, MaintenanceSchedule, Allocation, Maintenance
from .filters import ComponentFilter
from users.models import User
from .forms import (ComponentForm, MaintenanceForm, MaintenanceScheduleForm, 
CompanyForm, DivisionForm, BranchForm, PositionForm, GroupForm, SystemForm, 
TypeForm, SubTypeForm, AllocationForm, VendorForm)
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


@login_required
def component_create_view(request):

    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        modal_form = MaintenanceScheduleForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'], '{}/% Y/% m/% d/'.format(MEDIA_URL))
                form.save()
                messages.success(request, _("Component added successfully!"))
                return redirect('asset_app:component_list_view')
            except Exception as e:
                messages.error(request, _("Error: {}.".format(e.args)))

        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = ComponentForm()
    modal_form = MaintenanceScheduleForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/createviews/component_create.html', context)


@login_required
def maintenance_create_view_old(request):
 
    if request.method == 'POST': 
        form = MaintenanceForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by =  instance.modified_by = request.user
            instance.created = instance.modified = datetime.datetime.now()
            instance = instance.save()
            messages.success(request, _("'{}' added successfully!".format(request.POST.get('name'))))
            return redirect('/')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'asset_app/createviews/maintenance_create.html', {'form': form})
    else:
        form = MaintenanceForm()

        maintenance = Maintenance.objects.all()
        context = {'form': form, 'maintenance': maintenance}
        return render(request, 'asset_app/createviews/maintenance_create.html', context)

@login_required
def maintenance_create_view(request):
    
    # request should be ajax and method should be POST.
    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by =  instance.modified_by = request.user
            instance.created = instance.modified = datetime.datetime.now()
            instance = instance.save()
            
            if request.POST.get('save_maintenance'):
                messages.success(request, _("'{}' added successfully!".format(request.POST.get('name'))))
                return redirect('/')
            else:
                return JsonResponse({"instance": instance}, status=200)
        
        else:
            if request.POST.get('save_maintenance'):
                for error in form.errors.values():
                    messages.error(request, error)
                return render(request, 'asset_app/createviews/maintenance_create.html', {'form': form})
            else:
                return JsonResponse({"error": form.errors}, status=400) 
    else:
        # If request is not POST    
        form = MaintenanceForm()

        maintenance = Maintenance.objects.all()
        context = {'form': form, 'maintenance': maintenance}
        return render(request, 'asset_app/createviews/maintenance_create.html', context)


def maintenance_ajax_view(request):
    
    print('Estou a correr')
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = MaintenanceForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            name = request.POST.get('id_name')
            type = request.POST.get('id_type')
            schedule = request.POST.get('id_schedule')
            frequency = request.POST.get('id_frequency')
            time_allocated = request.POST.get('id_time_allocated')
            action = request.POST.get('id_action')
            item_used = request.POST.get('id_item_used')
            quantity = request.POST.get('id_quantity')
            notes = request.POST.get('id_notes')
            
            instance = instance.save(commit=False)
            instance.created_by =  instance.modified_by = request.user
            instance.name = name
            instance.type = type
            instance.schedule = schedule
            instance.frequency = frequency
            instance.time_allocated = time_allocated
            instance.action = action
            instance.item_used = item_used
            instance.quantity = quantity
            instance.notes = notes
            instance.created = instance.modified = datetime.datetime.now()
            instance = instance.save()
            instance = form.save()
            
            return JsonResponse({"instance": instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def maintenance_schedule_create_view(request):
    
    if request.POST.get('save_maintenance'):
        modal_form = MaintenanceForm(request.POST)
        if modal_form.is_valid() and request.is_ajax():
            try:
                modal_form.save()
                return redirect("asset_app:maintenance_schedule_create")
            except Exception as e:
                modal_form = MaintenanceForm()
                return redirect("asset_app:maintenance_schedule_create")

    if request.POST.get('save_maintenance_schedule'):  
        form = MaintenanceScheduleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Maintenance Schedule added successfully!"))
                return redirect('asset_app:maintenance_schedule_list_view')
            except Exception as e:
                messages.error(request, _("Error: {}".format(e.args)))
                return redirect('asset_app:maintenance_schedule_create')
            
    form = MaintenanceScheduleForm()
    modal_form = MaintenanceForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/maintenance_schedule_create.html', context)


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
    return render(request, 'asset_app/company_create.html', context)


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
    return render(request, 'asset_app/division_create.html', context)


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
    return render(request, 'asset_app/branch_create.html', context)


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
    return render(request, 'asset_app/position_create.html', context)


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
    return render(request, 'asset_app/group_create.html', context)


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
    return render(request, 'asset_app/system_create.html', context)


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
    return render(request, 'asset_app/type_create.html', context)


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
    return render(request, 'asset_app/subtype_create.html', context)


def vendor_create_view(request):
    if request.method == 'POST' and 'save_vendor':
        form = VendorForm(request.POST)
       
        if form.is_valid() and 'save_vendor':
            form.save()
            messages.success(request, _("Vendor added successfully!"))
            return redirect('/')
      
    form = VendorForm()
    context = {'form': form,}
    return render(request, 'asset_app/vendor_create.html', context)


def component_allocation_create_view(request):
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
    context = {'form': form, 'modal_form': vendor_form, "group_form": group_form,
    "system_form": system_form, "type_form": type_form, "subtype_form": subtype_form,
    "company_form": company_form, "division_form": division_form, "branch_form": branch_form ,
    "position_form": position_form, 'component_form': component_form}
    return render(request, 'asset_app/component_allocation_create.html', context)

###################### ************ LIST VIEWS ************  ######################

class ComponentListView(ListView):
    model = Component
    template_name = 'asset_app/listviews/component_list_view.html'


class MaintenanceScheduleListView(ListView):
    model = MaintenanceSchedule
    template_name = 'asset_app/listviews/maintenance_schedule_list_view.html'


class AllocationListView(ListView):
    model = Allocation
    template_name = 'asset_app/listviews/component_allocation_list_view.html'


###################### ************ DELETE VIEWS ************  ######################

def delete_component_view(request):

    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        for i, id in enumerate(selected_ids):
            if id != '':
                Component.objects.filter(id__in=selected_ids).delete()
        
        messages.success(request, _("Component(s) delete successfully!"))
        return redirect('asset_app:component_list_view')

def delete_maintenance_schedule_view(request):

    if request.is_ajax():
        selected_ids = request.POST['ckeck_box_item_ids']
        selected_ids = json.loads(selected_ids)
        
        for i, id in enumerate(selected_ids):
            if id != '':
                MaintenanceSchedule.objects.filter(id__in=selected_ids).delete()
       
        if len(selected_ids) == 1:
            messages.success(request, _("Schedule delete successfully!"))
        else:
            messages.success(request, _("{} Schedule(s) delete successfully!".format(len(selected_ids))))

    return redirect('asset_app:asset_app_home')

###################### ************ UPDATE VIEWS ************  ######################

# update view for details
def component_update_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Component, slug=slug)
 
    # pass the object as instance in form
    form = ComponentForm(request.POST or None, instance = obj)
    modal_form = MaintenanceScheduleForm(request.POST or None)

    if modal_form.is_valid():
        modal_form.save()
        modal_opened = True
    else:
        modal_opened = False

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, _("Data updated successfully!"))
        return redirect('asset_app:component_list_view')
    else:
        if modal_opened is False:
            messages.error(request, list(form.errors.values()))
 
    # add form dictionary to context
    context["form"] = form
    context["modal_form"] = modal_form
 
    return render(request, "asset_app/component_create.html", context)


###################### ************ DETAIL VIEWS ************  ######################
# after updating it will redirect to detail_View
def component_detail_view(request, slug):
    # dictionary for initial data with
    # field names as keys
    context ={}
  
    # add the dictionary during initialization
    context["data"] = Component.objects.get(slug=slug)
          
    return render(request, "asset_app/component_detail_view.html", context)

