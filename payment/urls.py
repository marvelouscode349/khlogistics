from django.urls import path

from . import views


urlpatterns = [
    path('make', views.addpayment, name='add-payment'),
    path('payments', views.all_payment, name='all-payment'),
    path('confirm', views.makepayment, name='confirm-payment'),
    path('insert', views.insertpayment, name='insert-payment'),
    path('success', views.payment_successful, name='payment-successful'),
   
]
