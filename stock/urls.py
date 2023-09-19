from django.urls import path

from . import views


urlpatterns = [
    path('add', views.addstock, name='add-stock'),
    path('', views.allstock, name='all-stock'),
    path('vendor/all', views.vendor_stock, name='vendor-stock'),
    path('approve/<user>/<pk>', views.approve_stock, name='approve-stock'),
    path('approved', views.approved_stock, name='approved-stock'),
    path('unapproved', views.unapproved_stock, name='unapproved-stock'),
]
