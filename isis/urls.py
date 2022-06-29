from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (product_create_view, product_list_view, product_update_view, product_delete_view, 
product_detail_view, product_dashboard_view, tax_create_view, tax_list_view, tax_update_view, tax_delete_view,
tax_detail_view, invoice_create_view, invoice_list_view, invoice_update_view, invoice_delete_view, 
invoice_detail_view, receipt_create_view, ReceiptListView, receipt_update_view, receipt_delete_view, 
payment_method_create_view, payment_method_list_view, receipt_invoice_view, 
payment_method_update_view, payment_method_delete_view, 
payment_term_create_view, payment_term_list_view, payment_term_update_view, payment_term_delete_view, 
invoice_item_create_view, invoice_item_delete_view, invoice_show, load_sell_prices,
category_create_view, CategoryListView, category_update_view, category_delete_view,
category_detail_view,
)

app_name = 'isis'

urlpatterns = [
    path('categories/new/', category_create_view, name='category_create'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/update/', category_update_view, name='category_update'),
    path('categories/delete/', category_delete_view, name='category_delete'),
    path('categories/<slug:slug>/', category_detail_view, name='category_details'),
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
    path('receipts/', ReceiptListView.as_view(), name='receipt_list'),
    path('receipts/<slug:slug>/update/', receipt_update_view, name='receipt_update'),
    path('receipts/delete/', receipt_delete_view, name='receipt_delete'),
    path('receipts/<slug:slug>/items/', receipt_invoice_view, name='receipt_invoice'),
    path('taxes/new/pk:pk/', tax_create_view, name='tax_create'),
    path('taxes/', tax_list_view, name='tax_list'),
    path('taxes/<slug:slug>/update/', tax_update_view, name='tax_update'),
    path('taxes/delete/', tax_delete_view, name='tax_delete'),
    path('taxes/<slug:slug>/', tax_detail_view, name='tax_details'),
    path('payment_methods/new/', payment_method_create_view, name='payment_method_create'),
    path('payment_methods/', payment_method_list_view, name='payment_method_list'),
    path('payment_methods/<slug:slug>/update/', payment_method_update_view, name='payment_method_update'),
    path('payment_methods/delete/', payment_method_delete_view, name='payment_method_delete'),
    path('payment_terms/new/', payment_term_create_view, name='payment_term_create'),
    path('payment_terms/', payment_term_list_view, name='payment_term_list'),
    path('payment_terms/<slug:slug>/update/', payment_term_update_view, name='payment_term_update'),
    path('payment_terms/delete/', payment_term_delete_view, name='payment_term_delete'),

    path('ajax/load-prices/', load_sell_prices, name='ajax_load_prices'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

