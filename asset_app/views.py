from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import Component
from .filters import ComponentFilter
from users.models import User
from .forms import (ComponentForm, MaintenanceForm, MaintenanceScheduleForm, 
CompanyForm, DivisionForm, BranchForm, PositionForm, GroupForm, SystemForm, 
TypeForm, SubTypeForm, ComponentAllocationForm)
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

        print(form.errors)

        if form.is_valid():
            form.save()
            messages.success(request, _("Component added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = ComponentForm()
    context = {'form': form}
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
        if form.is_valid():
            form.save()
            messages.success(request, _("Maintenance Schedule added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = MaintenanceScheduleForm()
    context = {'form': form}
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
        if form.is_valid():
            form.save()
            messages.success(request, _("Division added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = DivisionForm()
    context = {'form': form}
    return render(request, 'asset_app/division_create.html', context)


def branch_create_view(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Branch added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = BranchForm()
    context = {'form': form}
    return render(request, 'asset_app/branch_create.html', context)


def position_create_view(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Position added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = PositionForm()
    context = {'form': form}
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
        if form.is_valid():
            form.save()
            messages.success(request, _("System added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))
            
    form = SystemForm()
    context = {'form': form}
    return render(request, 'asset_app/system_create.html', context)


def type_create_view(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, _("Type added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = TypeForm()
    context = {'form': form}
    return render(request, 'asset_app/type_create.html', context)


def subtype_create_view(request):
    if request.method == 'POST':
        form = SubTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("SubType added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = SubTypeForm()
    context = {'form': form}
    return render(request, 'asset_app/subtype_create.html', context)


def component_allocation_create_view(request):
    if request.method == 'POST':
        form = ComponentAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Component Allocation added successfully!"))
            return redirect('/')
        else:
            messages.error(request, list(form.errors.values()))

    form = ComponentAllocationForm()
    context = {'form': form}
    return render(request, 'asset_app/component_allocation_create.html', context)


