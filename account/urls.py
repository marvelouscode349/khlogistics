from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
urlpatterns = [
path('signup', views.register, name='register'),
path('resend_verification_email', views.resend_verification_email, name='resend_verification_email'),
path('login', views.login, name='login'),
path('activate/<uidb64>/<token>', views.activate, name='activate'),
path('profile', views.profile, name='profile'),
path('profile/admins', views.adminprofile, name='admin-profile'),
path('timeout', views.timeout, name='timeout'),


path('logout', auth_view.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


]