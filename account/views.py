from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from . models import Account
from django.contrib import messages, auth
from django.http import HttpResponse

#verification

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

#register user
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            
            

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            if request.user.is_authenticated and request.user.is_superadmin:
                user.designation = 'RIDER'

            else:
                user.designation = 'ADMIN'
            user.save()

          

            #user activation

            try:
                current_site = get_current_site(request)
                mail_subject = "please activate your account"
                message =render_to_string('user/verify_account.html', {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)

            })

                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email],)
                send_email.send()
                return redirect('login')

            

            except Exception as e:
                 messages.error(request, 'Email could not be sent. Please try again.')
                 return redirect('resend_verification_email?email='+email)

                 


            messages.success(request, "Registration successful")
            return redirect('login?command=verification&email='+email)
    else:
        form = RegistrationForm()


    
    context = {'form':form}
    return render(request, 'user/register.html', context)


def resend_verification_email(request):
    email = request.GET.get('email')
    user = Account.objects.get(email=email)
    
    if request.method == 'POST':
        

        try:
            current_site = get_current_site(request)
            mail_subject = "please activate your account"
            message =render_to_string('user/verify_account.html', {
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)

        })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email],)
            send_email.send()
            return redirect('login')
        

        except Exception as e:
            messages.error(request, 'Email could not be sent. Please try again.')
            return redirect('resend_verification_email?email='+email)
    return render(request, 'user/resend_verification_email.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True

        user.is_admin = True

        user.save()
        messages.success(request, "your account has being activated, you can proceed to login.")
        return redirect('login')
    else:
        messages.error(request, "invalid activation link")
        return redirect('register')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superadmin:
                  messages.success(request, f"welcome {user.username} login successful")
                  return redirect('admin-dashboard')

            elif  user.designation == 'RIDER':
                #  messages.success(request, f"welcome {user.username} login successful")
                  return redirect('rider-dashboard')

               

            else:
                 if user.is_verified == False:
                   return redirect('login?command=verification&email='+email)
                 elif user.is_approved == False:
                    return redirect('profile')

                 else:
                  messages.success(request, f"welcome {user.username} login successful")
                  return redirect('vendor-dashboard')

           
        else:
            
            messages.error(request, "invalid login credentials")
            return redirect('login')
    return render(request, 'user/login.html')

def profile(request):
    if request.method=='POST':

        userform = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile,)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect('profile')
    else:
        userform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm( instance=request.user.profile,)

    context = {'userform':userform, 'profileform':profileform}
    return render(request, 'admin/main_profile.html', context)


def timeout(request):
    return render(request, 'user/timeout.html')

