from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account
from payment.models import payment
from order.models import Order
from stock.models import Stock
from django.db.models import Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

@login_required(login_url = 'login')
def admin_dashboard(request):
     users = Account.objects.all().filter(is_superadmin=False).count()
     approved = Account.objects.all().filter(is_approved=True, is_superadmin=False).count()
     unapproved = Account.objects.all().filter(is_approved=False, is_superadmin=False).count()
     stock=Stock.objects.all()
     stock_count = stock.count()
     total_stock_quantity = 0
     for stock in stock:
        total_stock_quantity += stock.stock_quantity
     orders = Order.objects.all().order_by('-id')[:5]
     order_count = Order.objects.all().count()
     pending_order = Order.objects.filter(status='pending').count()
     payments = payment.objects.all().order_by('-id')[:6]

     context = {
        'payments':payments,
        'users':users, 
        'approved':approved,
        'unapproved':unapproved,
        'stock_count':stock_count,
        'total_stock_quantity':total_stock_quantity,
        'pending_order':pending_order,
        'order_count':order_count,
        'orders':orders

     }
     return render(request, 'admin/admin_dashboard.html', context)

@login_required(login_url = 'login')
def vendor_dashboard(request):
    user = request.user
    stock = Stock.objects.filter(user=user, is_approved=True)
    stock_count = Stock.objects.filter(user=user, is_approved=True).count()
    unapproved_stock = Stock.objects.filter(user=user, is_approved=False).count()
    
    vendor_stock_quntity = 0
    for stock in stock:
        vendor_stock_quntity += stock.stock_quantity

    user = request.user
    orders = Order.objects.filter(status='completed', user=user)
    allorder_count = Order.objects.filter(user = user).count()
    pendingorder_count = Order.objects.filter(user = user, status='pending').count()
    order_count = orders.count()
    recent_orders = Order.objects.filter(user=user).order_by('-id')[:6]
    context = {
       
        'stock_count': stock_count,
        'vendor_stock_quntity': vendor_stock_quntity,
        'unapproved_stock':unapproved_stock,
        'order_count':order_count,
        'allorder_count':allorder_count,
        'pendingorder_count':pendingorder_count,
        'recent_orders':recent_orders

     }
    return render(request, 'admin/vendor_dashboard.html', context)


@login_required(login_url = 'login')
def rider_dashboard(request):

    user = request.user
    order = Order.objects.filter(rider=user)
    context = {'order':order}

    return render(request, 'admin/rider_order.html', context)


@login_required(login_url = 'login')
def rider_pending(request):
    user = request.user

    order = Order.objects.filter(status = 'pending', rider=user)
    context = {'order':order}
    return render(request, 'admin/rider_pending.html',context)


@login_required(login_url = 'login')
def all_users(request):
    users = Account.objects.all().filter(is_superadmin=False, designation='ADMIN')
    context = {'users':users}
    return render(request, 'admin/all_users.html', context)

@login_required(login_url = 'login')
def approved_users(request):
    users = Account.objects.all().filter(is_superadmin=False, is_approved=True)
    context = {'users':users}
    return render(request, 'admin/approved_users.html', context)


@login_required(login_url = 'login')
def unapproved_users(request):
    users = Account.objects.all().filter(is_superadmin=False, is_approved=False)
    context = {'users':users}
    return render(request, 'admin/unapproved_users.html', context)

@login_required(login_url = 'login')   
def user_detail(request, email):
    vendor = Account.objects.get(email=email)
    context = {'vendor':vendor}
    return render(request, 'admin/vendor_profile.html', context)


@login_required(login_url = 'login')
def approve_user(request, email):
    vendor =  Account.objects.get(email=email)
    vendor.is_approved = True
    vendor.save()

    #send email to user
    current_site = get_current_site(request)
    mail_subject = "Account approval"
    message =render_to_string('user/approve_account.html', {
    'vendor':vendor,
    'domain':current_site,
    
    

            })

    to_email = vendor.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    messages.success(request, f"{vendor.username} has being approved")
    return redirect('all-users')


@login_required(login_url = 'login')
def reject_user(request, email):
    vendor =  Account.objects.get(email=email)
    vendor.is_approved = False
    vendor.save()

    #send email to user
    current_site = get_current_site(request)
    mail_subject = "Account has not being approved"
    message =render_to_string('user/reject_account.html', {
    'vendor':vendor,
    'domain':current_site,
    
    

            })

    to_email = vendor.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    messages.success(request, f"{vendor.username} has being rejected")
    return redirect('all-users')


@login_required(login_url = 'login')
def search(request):

    if request.method == 'POST':
        name = request.POST.get('search').strip()
        
        users = Account.objects.filter(Q(username__icontains = name)| Q(email__icontains = name) )
        searchcount = users.count()
        result = ''
        if searchcount > 0:
            result = searchcount
        else:
            result = 0
        context = {'users':users, 'result':result}
    return render(request, 'admin\search.html', context)


