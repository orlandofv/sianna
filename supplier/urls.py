from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (invoice_create_view, invoice_list_view, invoice_update_view, invoice_delete_view, 
invoice_detail_view,  invoice_item_create_view, invoice_item_delete_view,
SupplierListView, supplier_create_view, supplier_update_view, supplier_delete_view, supplier_detail_view)


app_name = 'supplier'


urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/new/',supplier_create_view, name='supplier_create'),
    path('suppliers/<slug:slug>/update/', supplier_update_view, name='supplier_update'),
    path('suppliers/delete/', supplier_delete_view, name='supplier_delete'),
    path('suppliers/<slug:slug>/', supplier_detail_view, name='supplier_details'),
    path('supplier/invoices/new/', invoice_create_view, name='invoice_create'),
    path('supplier/invoices/', invoice_list_view, name='invoice_list'),
    path('supplier/invoices/<slug:slug>/update/', invoice_update_view, name='invoice_update'),
    path('supplier/invoices/delete/', invoice_delete_view, name='invoice_delete'),
    path('supplier/invoices/<slug:slug>/', invoice_detail_view, name='invoice_details'),
    path('supplier/invoices/<slug:slug>/items/', invoice_item_create_view, name='invoice_item_create'),
    path('supplier/invoices/items/delete/', invoice_item_delete_view, name='invoice_item_delete'),
]

