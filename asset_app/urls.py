from django.urls import path
from django.conf.urls import url
from .views import (home_view, component_create_view, maintenance_create_view, 
maintenance_schedule_create_view, company_create_view, division_create_view, 
branch_create_view, position_create_view, group_create_view, system_create_view, 
type_create_view, subtype_create_view, component_allocation_create_view)

app_name = 'asset_app'

urlpatterns = [
    path('', home_view, name='asset_app_home'),
    path('component/new', component_create_view, name='component_create'),
    path('maintenance/new', maintenance_create_view, name='maintenance_create'),
    path('maintenance_schedule/new', maintenance_schedule_create_view, name='maintenance_schedule_create'),
    path('company/new', company_create_view, name='company_create'),
    path('division/new', division_create_view, name='division_create'),
    path('branch/new', branch_create_view, name='branch_create'),
    path('position/new', position_create_view, name='position_create'),
    path('group/new', group_create_view, name='group_create'),
    path('system/new', system_create_view, name='system_create'),
    path('type/new', type_create_view, name='type_create'),
    path('subtype/new', subtype_create_view, name='subtype_create'),
    path('component_allocation/new', component_allocation_create_view, name='component_allocation_create'),
]

