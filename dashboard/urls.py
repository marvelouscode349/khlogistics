from django.urls import path
from . import views



urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
    path('vendor/', views.vendor_dashboard, name='vendor-dashboard'),
    path('vendors/', views.all_users, name='all-users'),
    path('vendors/detail/<email>', views.user_detail, name='user-detail'),
    path('vendors/approve/<email>', views.approve_user, name='user-approve'),
    path('vendors/reject/<email>', views.reject_user, name='user-reject'),
    path('vendors/confirmed', views.approved_users, name='approved'),
    path('vendors/unconfirmed', views.unapproved_users, name='unapproved'),
    path('vendors/search', views.search, name='search'),
    path('rider', views.rider_dashboard, name='rider-dashboard'),
    path('rider/pending', views.rider_pending, name='rider-pending')

    
    

]