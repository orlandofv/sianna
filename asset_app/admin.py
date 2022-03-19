from django.contrib import admin
from .models import (Component, Company, ComponentAllocation, 
Maintenance, MaintenanceSchedule, Division, Branch, Position, 
Group, System, Type, SubType)


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('component_name', 'component_manufacturer', 'component_stock_code', 'notes',)
    

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_address', 'company_manager', 'company_contacts', 'notes',)
  

class ComponentAllocationAdmin(admin.ModelAdmin):
    list_display = ('component_name', 'company_name', 'date_allocated','component_serial_number', 
    'component_status', 'notes',)


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('maintenance_frequency', 'maintenance_schedule', 'maintenance_type', 
    'time_allocated', 'maintenance_action')


class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_name', 'maintenance_name')


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('division_name', 'company_name', 'division_address', 'division_contacts', 'notes',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'division_name', 'notes',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'branch_name', 'notes',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'notes',)


class SystemAdmin(admin.ModelAdmin):
    list_display = ('system_name', 'group_name', 'notes',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'system_name', 'notes',)


class SubtypeAdmin(admin.ModelAdmin):
    list_display = ('subtype_name', 'type_name', 'notes',)


admin.site.register(Component, ComponentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(SubType, SubtypeAdmin)
admin.site.register(ComponentAllocation, ComponentAllocationAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceSchedule, MaintenanceScheduleAdmin)

