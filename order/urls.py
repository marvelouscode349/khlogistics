from django.urls import path

from . import views


urlpatterns = [
    path('request', views.addorder, name='add-order'),
    path('vendor/uncomplete', views.uncompleted_order, name='vendor-uncompleted-order'),
    path('admin/uncomplete', views.admin_uncompleted_order, name='uncompleted-orders'),
    path('admin/complete', views.admin_completed_order, name='completed-orders'),
    path('vendor/complete', views.vendor_completed_order, name='vendor-completed-orders'),
    path('vendor/pending', views.vendor_pending_order, name='vendor-pending-orders'),
    path('admin/all', views.allorder, name='all-orders'),
    path('assign', views.assignrider, name='assign'),
    path('vendor/order', views.vendor_orders, name='vendor-orders'),
    path('confirm/<int:order_id>', views.order_confirm, name='confirm-orders'),
    path('reject/<int:order_id>', views.reject_order, name='reject-order'),
    path('confirm/assign/<int:order_id>', views.confirm_assign, name='assign-confirm-order'),
    path('admin/complete_order/<user>/<order_pk>/<order_name>', views.complete_order, name='complete-order'),
    
]
