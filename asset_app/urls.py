from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.conf.urls import url
from .views import (home_view, 
ComponentListView, component_delete_view, component_update_view, component_detail_view, component_create_view,
MaintenanceListView, maintenance_delete_view, maintenance_create_view,  maintenance_detail_view,
maintenance_update_view, maintenance_item_delete_view, maintenance_item_create_view, maintenance_dashboard_view, 
maintenance_action_delete_view,
CompanyListView, company_update_view, company_delete_view, company_detail_view, company_create_view,
component_dashboard_view,
DivisionListView, division_update_view, division_delete_view, division_detail_view, division_create_view,
BranchListView, branch_update_view, branch_delete_view, branch_create_view, branch_detail_view,
PositionListView, position_create_view, position_update_view, position_delete_view, position_detail_view,
GroupListView, group_update_view, group_delete_view, group_detail_view, group_create_view,
SystemListView, system_update_view, system_delete_view, system_create_view, system_detail_view,
TypeListView, type_create_view, type_update_view, type_delete_view, type_detail_view,
VendorListView, vendor_create_view, vendor_update_view, vendor_delete_view, vendor_detail_view,
SubTypeListView, subtype_create_view, subtype_update_view, subtype_delete_view, subtype_detail_view,
AllocationListView, allocation_create_view, allocation_update_view, allocation_delete_view, allocation_detail_view,
WorkOrderListView, workorder_create_view, workorder_update_view, workorder_delete_view, workorder_detail_view,
settings_create_view,)


app_name = 'asset_app'


urlpatterns = [
    path('', home_view, name='home'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenances/new', maintenance_create_view, name='maintenance_create'),
    path('maintenances/<slug:slug>/update', maintenance_update_view, name='maintenance_update'),
    path('maintenances/delete', maintenance_delete_view, name='maintenance_delete'),
    path('maintenances/<slug:slug>', maintenance_detail_view, name='maintenance_details'),
    path('maintenances/dashboard/', maintenance_dashboard_view, name='maintenance_dashboard'),
    path('items/<slug:slug>/new', maintenance_item_create_view, name='item_create'),
    path('items/delete', maintenance_item_delete_view, name='item_delete'),
    path('actions/delete', maintenance_action_delete_view, name='action_delete'),
    path('components/', ComponentListView.as_view(), name='component_list'),
    path('components/new', component_create_view, name='component_create'),
    path('components/<slug:slug>/update', component_update_view, name='component_update'),
    path('components/dashboard', component_dashboard_view, name='component_dashboard'),
    path('components/delete', component_delete_view, name='component_delete'),
    path('components/<slug:slug>', component_detail_view, name='component_details'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/new', company_create_view, name='company_create'),
    path('companies/<slug:slug>/update', company_update_view, name='company_update'),
    path('companies/delete', company_delete_view, name='company_delete'),
    path('companies/<slug:slug>', company_detail_view, name='company_details'),
    path('divisions/', DivisionListView.as_view(), name='division_list'),
    path('divisions/new', division_create_view, name='division_create'),
    path('divisions/<slug:slug>/update', division_update_view, name='division_update'),
    path('divisions/delete', division_delete_view, name='division_delete'),
    path('divisions/<slug:slug>', division_detail_view, name='division_details'),
    path('branches/', BranchListView.as_view(), name='branch_list'),
    path('branches/new', branch_create_view, name='branch_create'),
    path('branches/<slug:slug>/update', branch_update_view, name='branch_update'),
    path('branches/delete', branch_delete_view, name='branch_delete'),
    path('branches/<slug:slug>', branch_detail_view, name='branch_details'),
    path('positions/', PositionListView.as_view(), name='position_list'),
    path('positions/new', position_create_view, name='position_create'),
    path('positions/<slug:slug>/update', position_update_view, name='position_update'),
    path('positions/delete', position_delete_view, name='position_delete'),
    path('positions/<slug:slug>', position_detail_view, name='position_details'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/new', group_create_view, name='group_create'),
    path('groups/<slug:slug>/update', group_update_view, name='group_update'),
    path('groups/delete', group_delete_view, name='group_delete'),
    path('groups/<slug:slug>', group_detail_view, name='group_details'),
    path('systems/', SystemListView.as_view(), name='system_list'),
    path('systems/new', system_create_view, name='system_create'),
    path('systems/<slug:slug>/update', system_update_view, name='system_update'),
    path('systems/delete', system_delete_view, name='system_delete'),
    path('systems/<slug:slug>', system_detail_view, name='system_details'),
    path('types/', TypeListView.as_view(), name='type_list'),
    path('types/new', type_create_view, name='type_create'),
    path('types/<slug:slug>/update', type_update_view, name='type_update'),
    path('types/delete', type_delete_view, name='type_delete'),
    path('types/<slug:slug>', type_detail_view, name='type_details'),
    path('subtypes/', SubTypeListView.as_view(), name='subtype_list'),
    path('subtypes/new', subtype_create_view, name='subtype_create'),
    path('subtypes/<slug:slug>/update', subtype_update_view, name='subtype_update'),
    path('subtypes/delete', subtype_delete_view, name='subtype_delete'),
    path('subtypes/<slug:slug>', subtype_detail_view, name='subtype_details'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/new', vendor_create_view, name='vendor_create'),
    path('vendors/<slug:slug>/update', vendor_update_view, name='vendor_update'),
    path('vendors/delete', vendor_delete_view, name='vendor_delete'),
    path('vendors/<slug:slug>', vendor_detail_view, name='vendor_details'),
    path('allocations/', AllocationListView.as_view(), name='allocation_list'),
    path('allocations/new', allocation_create_view, name='allocation_create'),
    path('allocations/<slug:slug>/update', allocation_update_view, name='allocation_update'),
    path('allocations/delete', allocation_delete_view, name='allocation_delete'),
    path('allocations/<slug:slug>', allocation_detail_view, name='allocation_details'),
    path('workorders/', WorkOrderListView.as_view(), name='workorder_list'),
    path('workorders/new', workorder_create_view, name='workorder_create'),
    path('workorders/<slug:slug>/update', workorder_update_view, name='workorder_update'),
    path('workorders/delete', workorder_delete_view, name='workorder_delete'),
    path('workorders/<slug:slug>', workorder_detail_view, name='workorder_details'),
    path('settings/', settings_create_view, name='settings_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

