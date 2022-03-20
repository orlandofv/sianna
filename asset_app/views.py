import json

from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import Component, MaintenanceSchedule
from .filters import ComponentFilter
from users.models import User
from .forms import (ComponentForm, MaintenanceForm, MaintenanceScheduleForm, 
CompanyForm, DivisionForm, BranchForm, PositionForm, GroupForm, SystemForm, 
TypeForm, SubTypeForm, ComponentAllocationForm, VendorForm)
from django.contrib import messages #import messages
from django.utils.translation import ugettext_lazy as _


def home_view(request):
    context = {
        'components': Component.objects.all()
    }
    return render(request, 'index.html', context)

def component_create_view(request):

    if request.method == 'POST':
        form = ComponentForm(request.POST)
        modal_form = MaintenanceScheduleForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Component added successfully!"))
            return redirect('asset_app:component_list_view')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = ComponentForm()
    modal_form = MaintenanceScheduleForm()
    context = {'form': form, 'modal_form': modal_form}
    return render(request, 'asset_app/component_create.html', context)


def maintenance_create_view(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, _("Maintenance added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = MaintenanceForm()
    context = {'form': form}
    return render(request, 'asset_app/maintenance_create.html', context)


def maintenance_schedule_create_view(request):
    
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)
        modal_form = MaintenanceForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Maintenance Schedule added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

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


def component_allocation_create_view(request):
    if request.method == 'POST':
        form = ComponentAllocationForm(request.POST)
        component_form = ComponentForm(request.POST)
        modal_form = VendorForm(request.POST)
        group_form = GroupForm(request.POST)
        system_form = SystemForm(request.POST)
        type_form = TypeForm(request.POST)
        subtype_form = SubTypeForm(request.POST)
        company_form = CompanyForm(request.POST)
        division_form = DivisionForm(request.POST)
        branch_form = BranchForm(request.POST)
        position_form = PositionForm(request.POST)

        if modal_form.is_valid():
            modal_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if component_form.is_valid():
            component_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if group_form.is_valid():
            group_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if system_form.is_valid():
            system_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if type_form.is_valid():
            type_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if subtype_form.is_valid():
            subtype_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if company_form.is_valid():
            company_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if division_form.is_valid():
            division_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if branch_form.is_valid():
            branch_form.save()
            modal_opened = True
        else:
            modal_opened = False
        
        if position_form.is_valid():
            position_form.save()
            modal_opened = True
        else:
            modal_opened = False

        if form.is_valid():
            form.save()
            messages.success(request, _("Component Allocation added successfully!"))
            return redirect('/')
        else:
            if modal_opened is False:
                messages.error(request, list(form.errors.values()))

    form = ComponentAllocationForm()
    component_form = ComponentForm()
    modal_form = VendorForm()
    group_form = GroupForm()
    system_form = SystemForm()
    type_form = TypeForm()
    subtype_form = SubTypeForm()
    company_form = CompanyForm()
    division_form = DivisionForm()
    branch_form = BranchForm()
    position_form = PositionForm()
    context = {'form': form, 'modal_form': modal_form, "group_form": group_form,
    "system_form": system_form, "type_form": type_form, "subtype_form": subtype_form,
    "company_form": company_form, "division_form": division_form, "branch_form": branch_form ,
    "position_form": position_form, 'component_form': component_form}
    return render(request, 'asset_app/component_allocation_create.html', context)

###################### ************ LIST VIEWS ************  ######################

class ComponentListView(ListView):
    model = Component
    template_name = 'asset_app/listviews/component_list_view.html'

###################### ************ DELETE VIEWS ************  ######################

def delete_component_view(request):

    if request.is_ajax():
        selected_tests = request.POST['test_list_ids']
        selected_tests = json.loads(selected_tests)
        for i, test in enumerate(selected_tests):
            if test != '':
                Component.objects.filter(id__in=selected_tests).delete()
        
        messages.success(request, _("Component(s) delete successfully!"))
        return redirect('asset_app:component_list_view')

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