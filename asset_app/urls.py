from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.conf.urls import url
from .views import (home_view, component_create_view, maintenance_create_view, 
maintenance_schedule_create_view, company_create_view, division_create_view, 
branch_create_view, position_create_view, group_create_view, system_create_view, 
type_create_view, subtype_create_view, allocation_create_view, 
component_delete_view, component_update_view, vendor_create_view,
component_detail_view, ComponentListView, maintenance_detail_view,
MaintenanceScheduleListView, MaintenanceListView, maintenance_schedule_detail_view,
AllocationListView, maintenance_item_create_view, item_delete_view, maintenance_delete_view, 
maintenance_schedule_delete_view, maintenance_update_view)

app_name = 'asset_app'

urlpatterns = [
    path('', home_view, name='home_view'),
    
    ################### Create Views
    path('components/new', component_create_view, name='component_create'),
    path('items/<slug:slug>/new', maintenance_item_create_view, name='item_create'),
    # path('maintenance_schedules/new', maintenance_schedule_create_view, name='maintenance_schedule_create'),
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
    path('allocations/new', allocation_create_view, name='allocation_create'),
    
    ################### List Views
    path('components/', ComponentListView.as_view(), name='component_list_view'),
    # path('maintenance_schedules/', MaintenanceScheduleListView.as_view(), name='maintenance_schedule_list_view'),
    path('allocations/', AllocationListView.as_view(), name='allocations_list_view'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenances_list_view'),
   
    ################### Delete Views
    path('components/delete', component_delete_view, name='component_delete_view'),
    path('items/delete', item_delete_view, name='item_delete_view'),
    # path('maintenance_schedules/delete', maintenance_schedule_delete_view, name='maintenance_schedule_delete_view'),
    path('maintenances/delete', maintenance_delete_view, name='maintenance_delete_view'),

    ################### Update Views
    path('components/<slug:slug>/update', component_update_view, name='component_update_view'),
    path('maintenances/<slug:slug>/update', maintenance_update_view, name='maintenance_update_view'),
    # path('maintenance_schedules/<slug:slug>/update', maintenance_update_view, name='schedule_update_view'),
    
    ################### Detail Views
    path('components/<slug:slug>', component_detail_view, name='component_detail_view'),
    path('maintenances/<slug:slug>', maintenance_detail_view, name='maintenance_detail_view'),
    # path('maintenance_schedules/<slug:slug>', maintenance_schedule_detail_view, name='schedule_detail_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

