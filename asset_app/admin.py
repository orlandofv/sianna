from django.contrib import admin
from .models import Assets, Location, AssetsIssuance, Category, System


class SystemAdmin(admin.ModelAdmin):
    list_display = ('system_name', 'category_id', 'notes',)
   

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'category_id', 'system_id', 'asset_serial_no', 'notes',)
    

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_address', 'location_manager', 'location_contacts', 'notes',)
  

class AssetIssuanceAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'asset_location', 'date_issued', 'asset_assignee', 'notes',)
  

admin.site.register(Assets, AssetAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Category)
admin.site.register(AssetsIssuance, AssetIssuanceAdmin)