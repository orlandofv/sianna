from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (product_create_view, product_list_view, product_update_view, product_delete_view, 
product_detail_view, product_dashboard_view, tax_create_view, tax_list_view, tax_update_view, tax_delete_view,
tax_detail_view, warehouse_create_view, warehouse_list_view, warehouse_update_view, warehouse_delete_view, warehouse_detail_view
, invoice_create_view, invoice_list_view, invoice_update_view, invoice_delete_view, 
invoice_detail_view, receipt_create_view, receipt_list_view, receipt_update_view, receipt_delete_view, 
payment_method_create_view, payment_method_list_view, payment_method_update_view, payment_method_delete_view, 
payment_term_create_view, payment_term_list_view, payment_term_update_view, payment_term_delete_view, 
invoice_item_create_view, invoice_item_delete_view, invoice_show,
)

app_name = 'isis'

urlpatterns = [
    path('products/new/', product_create_view, name='product_create'),
    path('products/', product_list_view, name='product_list'),
    path('products/<slug:slug>/update/', product_update_view, name='product_update'),
    path('products/delete/', product_delete_view, name='product_delete'),
    path('products/<slug:slug>/', product_detail_view, name='product_details'),
    path('products/dashboard/', product_dashboard_view, name='product_dashboard'),
    path('invoices/new/', invoice_create_view, name='invoice_create'),
    path('invoices/', invoice_list_view, name='invoice_list'),
    path('invoices/<slug:slug>/update/', invoice_update_view, name='invoice_update'),
    path('invoices/delete/', invoice_delete_view, name='invoice_delete'),
    path('invoices/<slug:slug>/', invoice_detail_view, name='invoice_details'),
    path('invoices/<slug:slug>/items/', invoice_item_create_view, name='invoice_item_create'),
    path('invoices/items/delete', invoice_item_delete_view, name='invoice_item_delete'),
    path('invoices/<slug:slug>/show/', invoice_show, name='invoice_show'),
    path('receipts/new/', receipt_create_view, name='receipt_create'),
    path('receipts/', receipt_list_view, name='receipt_list'),
    path('receipts/<slug:slug>/update/', receipt_update_view, name='receipt_update'),
    path('receipts/delete/', receipt_delete_view, name='receipt_delete'),
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
    path('payment_methods/new/', payment_method_create_view, name='payment_method_create'),
    path('payment_methods/', payment_method_list_view, name='payment_method_list'),
    path('payment_methods/<slug:slug>/update/', payment_method_update_view, name='payment_method_update'),
    path('payment_methods/delete/', payment_method_delete_view, name='payment_method_delete'),
    path('payment_terms/new/', payment_term_create_view, name='payment_term_create'),
    path('payment_terms/', payment_term_list_view, name='payment_term_list'),
    path('payment_terms/<slug:slug>/update/', payment_term_update_view, name='payment_term_update'),
    path('payment_terms/delete/', payment_term_delete_view, name='payment_term_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

