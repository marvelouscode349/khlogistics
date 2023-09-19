from django.shortcuts import render, redirect, HttpResponse
from . forms import AddOrder, order_complete
from stock.models import Stock
from . models import Order, order_complete as complete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import Account
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

@login_required(login_url = 'login')
def addorder(request):
    if request.method == 'POST':
      form = AddOrder(request.POST, user=request.user)
      if form.is_valid():
        stock_name = form.cleaned_data['stock']
        stocks = Stock.objects.get(stock_name=stock_name, user=request.user)
        if stocks.stock_quantity < form.cleaned_data['order_quantity']:

          messages.error(request, 'you stock quantity is not up to the order quantity you are requesting for')
          return redirect('add-order')
        instance = form.save(commit=False)
        instance.user = request.user
        quantity = form.cleaned_data['order_quantity']
        instance.order_size = stocks.stock_item_size * quantity
        price = form.cleaned_data['order_price']
        instance.order_price = price + (instance.order_size * 300)
        instance.save()

        order_id = instance.id
        
        stocks.stock_quantity -= form.cleaned_data['order_quantity']
        stocks.save()

        messages.success(request, 'your order has being placed')
        return redirect('confirm-orders', order_id = order_id )
        
    else:
        form = AddOrder(user=request.user)
    context = {'form':form}
    return render(request, 'admin/addorders.html', context)

@login_required(login_url = 'login')
def order_confirm(request, order_id):

  order = Order.objects.get(pk=order_id)
  price_size = order.stock.stock_item_size  * order.order_quantity *300
  price_distance = order.order_price - price_size
  context = {'order':order, 'price_size':price_size, 'price_distance':price_distance}


  return render(request, 'admin/order_confirm.html', context)

@login_required(login_url = 'login')
def reject_order(request, order_id):
  order = Order.objects.get(pk=order_id)
  order.delete()
  messages.success(request, 'order rejected please make your order again')

  return redirect('add-order')

@login_required(login_url = 'login')
def assignrider(request):
  if request.method == 'POST':
    form = AssignRider(request.POST)
    if form.is_valid():
      rider = form.cleaned_data['rider']
      order_id = request.POST['order_id']
      rider_info = Account.objects.get(email=rider)
      order = Order.objects.get(id=order_id)
      order.rider = rider
      order.status = 'pending'
      order.save()




      messages.success(request, f'order with name "{order.order_name}" to {order.order_la} has being assigned to rider "{rider_info.username}"')
      return redirect('uncompleted-orders')



@login_required(login_url = 'login')
def confirm_assign(request, order_id):
  order = Order.objects.get(pk=order_id)
  rider = Account.objects.filter(designation='RIDER')
  random_rider = random.choice(rider)
  order.rider = random_rider
  order.status = 'pending'
  order.save()

  #send email to user
  current_site = get_current_site(request)
  mail_subject = "Order Confirmation"
  message =render_to_string('admin/orders_confirm.html', {
    'order':order,
    'domain':current_site,
    
    

            })

  to_email = order.user.email
  send_email = EmailMessage(mail_subject, message, to=[to_email])

  send_email.send()

  return redirect('vendor-orders')

  



@login_required(login_url = 'login')
def allorder(request):
  if request.method == 'POST':

      if request.POST['vendor'] and request.POST['rider']:
          rider = request.POST['rider']
          vendor = request.POST['vendor']
          orders = Order.objects.filter(user = vendor, rider=rider).order_by('-id')

      elif request.POST['vendor']:

          vendor = request.POST['vendor']
          orders = Order.objects.filter(user = vendor).order_by('-id')
    
      elif request.POST['rider']:


          rider = request.POST['rider']
          orders = Order.objects.filter(rider = rider).order_by('-id')
      else:
        orders = Order.objects.all().order_by('-id')

  else:

    orders = Order.objects.all().order_by('-id')

  vendors = Account.objects.exclude(designation='RIDER')
  riders = Account.objects.filter(designation='RIDER')
  context = {'orders':orders, 'vendors':vendors, 'riders':riders}
  return render(request, 'admin/all_order.html', context)


@login_required(login_url = 'login')
def uncompleted_order(request):
  if request.method == 'POST':
       rider = request.POST.get('rider')
       vendor = request.POST('vendor')
       if vendor and rider:
         
         orders = Order.objects.filter(user = vendor, rider=rider).order_by('-id')

       elif vendor:

          vendor = request.POST['vendor']
          orders = Order.objects.filter(user = vendor).order_by('-id')
    
       elif rider:


          rider = request.POST['rider']
          orders = Order.objects.filter(rider = rider).order_by('-id')
       else:
        orders = Order.objects.all().order_by('-id')

  else:

    orders = Order.objects.all().order_by('-id')

  orders = Order.objects.filter(user=request.user, status=completed)
  context = {'orders':orders}
  return render(request, 'admin/uncompleted_order.html', context)

@login_required(login_url = 'login')
def admin_uncompleted_order(request):
     if request.method == 'POST':
        vendor = request.POST.get('vendor')
        rider = request.POST.get('rider')

        if vendor and rider:
            orders = Order.objects.filter(user=vendor, rider=rider).exclude(status='completed').order_by('-id')
        elif vendor:
            orders = Order.objects.filter(user=vendor).exclude(status='completed').order_by('-id')
        elif rider:
            orders = Order.objects.filter(rider=rider).exclude(status='completed').order_by('-id')
        else:
            orders = Order.objects.exclude(status='completed').order_by('-id')
     else:
        orders = Order.objects.exclude(status='completed').order_by('-id')

     vendors = Account.objects.exclude(designation='RIDER')
     riders = Account.objects.filter(designation='RIDER')

     context = {'orders': orders, 'vendors': vendors, 'riders': riders}
     return render(request, 'admin/admin_uncompleted_order.html', context)

@login_required(login_url = 'login')
def admin_completed_order(request):
  orders = complete.objects.all()
  context = {'orders':orders}
  return render(request, 'admin/admin_completed_order.html', context)

@login_required(login_url = 'login')
def vendor_completed_order(request):
  user = request.user
  orders = complete.objects.filter(order__user = user)
  context = {'orders':orders}
  return render(request, 'admin/vendor_completed_order.html', context)

@login_required(login_url = 'login')
def vendor_pending_order(request):
  user = request.user
  orders = Order.objects.filter(user = user, status='pending')
  context = {'orders':orders}
  return render(request, 'admin/vendor_pending_order.html', context)

@login_required(login_url = 'login')
def complete_order(request, user, order_pk, order_name):
  
   vendor = Account.objects.get(username = user)
   order = Order.objects.get(user=vendor, pk=order_pk, order_name=order_name)
   if request.method == 'POST':
     form = order_complete(request.POST, request.FILES)
     if form.is_valid():
      instance = form.save(commit=False)
      instance.order = order
      instance.save()
      order.status = 'completed'
      order.save()

      current_site = get_current_site(request)
      mail_subject = "Order Completion"
      message =render_to_string('admin/order_c.html', {
      'order':order,
      'domain':current_site,
    
    

            })
      
      to_email = order.user.email
      send_email = EmailMessage(mail_subject, message, to=[to_email])
      completeimage = complete.objects.get(order=order)
      image_content = completeimage.order_complete_image.read()
      image_filename = completeimage.order_complete_image.name
      send_email.attach(image_filename, image_content, 'image/jpeg' )
      send_email.send()


      if request.user.designation == 'RIDER':
         return redirect('rider-dashboard')

      
   else:
      form =  order_complete()
   

  
   context = {'order':order, 'vendor':vendor, 'form':form}
   return render(request, 'admin/rider_order_complete.html', context)



  

@login_required(login_url = 'login')
def vendor_orders(request):
  user = request.user
  orders = Order.objects.filter(user = user).order_by('-id')
  context = {'orders':orders}
  return render(request, 'admin/vendor_all_order.html', context)
  