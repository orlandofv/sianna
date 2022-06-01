from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import (invoice_create_view, invoice_list_view, invoice_update_view, invoice_delete_view, 
invoice_detail_view,  invoice_item_create_view, invoice_item_delete_view,)

app_name = 'supplier'

urlpatterns = [
    path('supplier/invoices/new/', invoice_create_view, name='invoice_create'),
    path('supplier/invoices/', invoice_list_view, name='invoice_list'),
    path('supplier/invoices/<slug:slug>/update/', invoice_update_view, name='invoice_update'),
    path('supplier/invoices/delete/', invoice_delete_view, name='invoice_delete'),
    path('supplier/invoices/<slug:slug>/', invoice_detail_view, name='invoice_details'),
    path('supplier/invoices/<slug:slug>/items/', invoice_item_create_view, name='invoice_item_create'),
    path('supplier/invoices/items/delete', invoice_item_delete_view, name='invoice_item_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

