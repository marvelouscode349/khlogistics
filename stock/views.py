from django.shortcuts import render, redirect
from . forms import AddStock
from django.contrib import messages
from . models import Stock
from account.models import Account
from django.db.models import Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

def addstock(request):
    if request.method == 'POST':
        addform = AddStock(request.POST, request.FILES)
        if addform.is_valid():
            instance = addform.save(commit=False)
            instance.user = request.user
            instance.save()

            messages.success(request, "your request to add stock is successful, wait till admin can confirm and approve your stock at the warehouse")
            return redirect('vendor-stock')
        else:
            print(addform.errors)

    else:
       addform = AddStock()
    context = {'addform':addform}
    return render(request, 'admin/addstock.html', context)


def approve_stock(request,user, pk):
    account = Account.objects.get(email=user)
    stock = Stock.objects.get(user=account, pk=pk)
    stock.is_approved = True
    stock.save()
    current_site = get_current_site(request)
    mail_subject = "Stock approval"
    message =render_to_string('stock/stock_approve.html', {
    'account':account,
    'domain':current_site,
            })
    to_email = account.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    messages.success(request, f"{stock.stock_name} with type {stock.stock_type} from {account.username} has being approved")
    return redirect('all-stock')


def allstock(request):
    stocks = Stock.objects.all()
    context = {'stocks':stocks}
    return render(request, 'admin/all_stock.html', context)


def vendor_stock(request):
    user = request.user
    stocks = Stock.objects.filter(user = user).order_by('-id')
    context = {'stocks':stocks}
    return render(request, 'admin/vendor_stock.html', context)

def approved_stock(request):
    stocks = Stock.objects.filter(is_approved=True)
    context = {'stocks':stocks}
    return render(request, 'admin/approved_stock.html', context)

def unapproved_stock(request):
    stocks = Stock.objects.filter(is_approved=False)
    context = {'stocks':stocks}
    return render(request, 'admin/unapproved_stock.html', context)
