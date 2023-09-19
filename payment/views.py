from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . forms import AddPayment
import uuid
import json
from . models import payment, Subscription
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from account.models import Account

# Cr=eate your views here.'

@login_required(login_url = 'login')
def addpayment(request):

    form = AddPayment()
    context = {'form':form}
    return render(request, 'admin/payment.html',context)

@login_required(login_url = 'login')
def makepayment(request):
    if request.method == 'POST':
        
        amount = request.POST.get('amount')
        payment_type = request.POST.get('payment_type')
        payment_id = uuid.uuid4()
        payment_plan = request.POST.get('payment_plan')

    context = {
        'amount':amount,
        'payment_type':payment_type,
        'payment_id':payment_id,
        'payment_plan':payment_plan


        
        }

    
    return render(request, "admin/pay_confirm.html", context)

@login_required(login_url = 'login')
def insertpayment(request):
    body = json.loads(request.body)

    # store transaction

    trans = payment(
        user = request.user,
        payment_id = body['payment_id'],
        amount=body['amount'],
        payment_type = body['payment_type'],
        payment_plan = body['payment_plan'],

        date=timezone.now()
    )

    trans.save()

    subscription_type = body['payment_plan']
    user_subscription, created = Subscription.objects.get_or_create(user=request.user, 
    defaults={'subscription_type': subscription_type, 'start_date': date.today()}
    )

    if created:
        # New subscription, set the start date
        user_subscription.start_date = date.today()

    if subscription_type == 'monthly':
        user_subscription.end_date = user_subscription.start_date + timedelta(days=30)
    elif subscription_type == '6-month':
        user_subscription.end_date = user_subscription.start_date + timedelta(days=30 * 6)
    elif subscription_type == 'yearly':
        user_subscription.end_date = user_subscription.start_date + timedelta(days=365)

    user_subscription.save()
    payment_id = body['payment_id']

    data = {
        'payment_id':payment_id
    }    
    
    return JsonResponse(data)

@login_required(login_url = 'login')
def payment_successful(request):
    payment_id = request.GET.get('payment_id')
    payment_details = payment.objects.get(payment_id=payment_id)
    context = {
        'payment_details':payment_details
    }
    return render(request, 'admin/payment_success.html', context)

@login_required(login_url = 'login')
def all_payment(request):
    payments = None
    if request.method == 'POST':
        user = request.POST.get('vendor')
        
        payments = payment.objects.filter(user=user)


    else:

        payments = payment.objects.all()
    vendor = Account.objects.exclude(designation='RIDER', is_superadmin=True)


    context = {
        'payments':payments,
        'vendor':vendor
    }
    
    return render(request, 'admin/payments_all.html', context)