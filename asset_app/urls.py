from django.urls import path
from django.conf.urls import url
from .views import (home_view, component_create_view, maintenance_create_view, 
maintenance_schedule_create_view, company_create_view, division_create_view, 
branch_create_view, position_create_view, group_create_view, system_create_view, 
type_create_view, subtype_create_view, component_allocation_create_view, 
delete_component_view, component_update_view, vendor_create_view,
component_detail_view, delete_maintenance_schedule_view, ComponentListView, 
MaintenanceScheduleListView, 
AllocationListView,  maintenance_ajax_view)

app_name = 'asset_app'

urlpatterns = [
    path('', home_view, name='asset_app_home'),
    
    ################### Create Views
    path('components/new', component_create_view, name='component_create'),
    path('maintenance_schedules/new', maintenance_schedule_create_view, name='maintenance_schedule_create'),
    path('companies/new', company_create_view, name='company_create'),
    path('maintenances/new', maintenance_create_view, name='maintenance_create'),
    path('divisions/new', division_create_view, name='division_create'),
    path('branches/new', branch_create_view, name='branch_create'),
    path('positions/new', position_create_view, name='position_create'),
    path('groups/new', group_create_view, name='group_create'),
    path('systems/new', system_create_view, name='system_create'),
    path('types/new', type_create_view, name='type_create'),
    path('subtypes/new', subtype_create_view, name='subtype_create'),
    path('vendors/new', vendor_create_view, name='vendor_create'),
    path('allocations/new', component_allocation_create_view, name='component_allocation_create'),
    
    ################### AJAX CREATE VIEWS ####################
    path('maintenance/ajax/save', maintenance_ajax_view, name='maintenance_ajax_save'),

    ################### List Views
    path('components/', ComponentListView.as_view(), name='component_list_view'),
    path('maintenance_schedules/', MaintenanceScheduleListView.as_view(), name='maintenance_schedule_list_view'),
    path('allocations/', AllocationListView.as_view(), name='allocations_list_view'),
   
    ################### Delete Views
    path('components/delete', delete_component_view, name='component_delete_view'),
    path('maintenance_schedules/delete', delete_maintenance_schedule_view, name='maintenance_schedule_delete_view'),

    ################### Update Views
    path('components/<slug:slug>/update', component_update_view, name='component_update_view'),
    
    ################### Detail Views
    path('components/<slug:slug>', component_detail_view, name='component_detail_view'),
]

