from django.contrib import admin
from .models import Assets, Location, AssetsIssuance, Category, System


class SystemAdmin(admin.ModelAdmin):
    list_display = ('system_name', 'category_id', 'notes',)
    prepopulated_fields = {'slug': ('system_name',)} # new

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'category_id', 'system_id', 'asset_serial_no', 'notes', )
    prepopulated_fields = {'slug': ('asset_name',)} # new

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_adress', 'location_manager', 'location_contacts', 'notes',)
    prepopulated_fields = {'slug': ('location_name',)} # new


admin.site.register(Assets, AssetAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Category)
admin.site.register(AssetsIssuance)