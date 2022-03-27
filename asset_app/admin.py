from django.contrib import admin
from .models import (Component, Company, 
Maintenance, MaintenanceSchedule, Division, Branch, Position, 
Group, System, Type, SubType, Vendor, Allocation)


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'stock_code', 'notes',)
    

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'schedule', 'type', 
    'time_allocated', 'action')


class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'maintenance')



class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager', 'contacts', 'notes',)


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'address', 'contacts', 'notes',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'notes',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'notes',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes',)


class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'notes',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'system', 'notes',)


class SubtypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'notes',)


class AllocationAdmin(admin.ModelAdmin):
    list_display = ('allocation_no', 'component', 'date_allocated','serial_number', 
    'status')


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes')


admin.site.register(Component, ComponentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(SubType, SubtypeAdmin)
admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceSchedule, MaintenanceScheduleAdmin)
admin.site.register(Vendor, VendorAdmin)


