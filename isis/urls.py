from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (product_create_view, product_list_view, product_update_view, product_delete_view, 
product_detail_view, product_dashboard_view, tax_create_view, tax_list_view, tax_update_view, tax_delete_view,
tax_detail_view, warehouse_create_view, warehouse_list_view, warehouse_update_view, warehouse_delete_view, warehouse_detail_view)

app_name = 'isis'

urlpatterns = [
    path('products/new/', product_create_view, name='product_create'),
    path('products/', product_list_view, name='product_list'),
    path('products/<slug:slug>/update/', product_update_view, name='product_update'),
    path('products/delete/', product_delete_view, name='product_delete'),
    path('products/<slug:slug>/', product_detail_view, name='product_details'),
    path('products/dashboard/', product_dashboard_view, name='product_dashboard'),
    path('taxes/new/', tax_create_view, name='tax_create'),
    path('taxes/', tax_list_view, name='tax_list'),
    path('taxes/<slug:slug>/update/', tax_update_view, name='tax_update'),
    path('taxes/delete/', tax_delete_view, name='tax_delete'),
    path('taxes/<slug:slug>/', tax_detail_view, name='tax_details'),
    path('warehouses/new/', warehouse_create_view, name='warehouse_create'),
    path('warehouses/', warehouse_list_view, name='warehouse_list'),
    path('warehouses/<slug:slug>/update/', warehouse_update_view, name='warehouse_update'),
    path('warehouses/delete/', warehouse_delete_view, name='warehouse_delete'),
    path('warehouses/<slug:slug>/', warehouse_detail_view, name='warehouse_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

