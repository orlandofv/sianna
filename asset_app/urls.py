from django.urls import path
from django.conf.urls import url
from .views import (
    AssetsListView,
    AssetsDetailView,
    AssetsCreateView,
    AssetsUpdateView,
    AssetsDeleteView,
)
from . import views

urlpatterns = [
    path('', AssetsListView.as_view(), name='assets_app_home'),
    path('asset/<slug:slug>/', AssetsDetailView.as_view(), name='asset_detail'),
    path('asset/new/', AssetsCreateView.as_view(), name='assets_create'),
    path('asset/<slug:slug>/update/', AssetsUpdateView.as_view(), name='asset_detail_update'),
    path('asset/<slug:slug>/delete/', AssetsDeleteView.as_view(), name='asset_detail_delete'),

    # path('location/<slug:slug>/', locationDetailView.as_view(), name='location_detail'),
    # path('location/new/', locationCreateView.as_view(), name='location_create'),
    # path('location/<slug:slug>/update/', locationUpdateView.as_view(), name='location_detail_update'),
    # path('location/<slug:slug>/delete/', locationDeleteView.as_view(), name='location_detail_delete'),

    # path('system/<slug:slug>/', systemDetailView.as_view(), name='system_detail'),
    # path('system/new/', systemCreateView.as_view(), name='system_create'),
    # path('system/<slug:slug>/update/', systemUpdateView.as_view(), name='system_detail_update'),
    # path('system/<slug:slug>/delete/', systemDeleteView.as_view(), name='system_detail_delete'),

    # path('category/<slug:slug>/', categoryDetailView.as_view(), name='category_detail'),
    # path('category/new/', categoryCreateView.as_view(), name='category_create'),
    # path('category/<slug:slug>/update/', categoryUpdateView.as_view(), name='category_detail_update'),
    # path('category/<slug:slug>/delete/', categoryDeleteView.as_view(), name='category_detail_delete'),

    # path('issuance/<slug:slug>/', issuanceDetailView.as_view(), name='issuance_detail'),
    # path('issuance/new/', issuanceCreateView.as_view(), name='issuance_create'),
    # path('issuance/<slug:slug>/update/', issuanceUpdateView.as_view(), name='issuance_detail_update'),
    # path('issuance/<slug:slug>/delete/', issuanceDeleteView.as_view(), name='issuance_detail_delete'),

    path('about/', views.about, name='app_about'),
    url(r'^searchassets/$', views.assetssearch, name='assetssearch'),
]
