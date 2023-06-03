from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import User, UserProfile
from .forms import RegisterUserForm, UserModelForm, UserProfileModelForm
from .utils import paginate_users

# Create your views here.
class UsersRegisterUser(View):
    def get(self, request):
        form = RegisterUserForm()
        context = {
           'next': 'core:index',
           'form': form
        }
        #return render(request, 'signup.html', context)
        return render( request, 'registration/signup.html', context)
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            found = True
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                found = False    

            if found == True:
                messages.error(request,'Username already exists.')
                context = {
                    'next': 'core:index',
                    'form': form
                }
                    
                return render( request, 'registration/signup.html', context)

            password = form.cleaned_data['password1']
            password_hash = make_password(password)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User(username=username,password=password_hash,first_name=first_name,last_name=last_name,email=email,is_staff=False,is_active=False,is_superuser=False)
            user.save()
            user.send_activation()
            messages.success(request, "User activation email has been sent.")
        else:
            messages.error(request,'Error in form validation.')
            context = {
                'next': 'core:index',
                'form': form
            }
                
            return render( request, 'registration/signup.html', context)
        return redirect('core:index')

class UsersActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated.')
            return redirect('core:index')
        else:
            messages.error(request, 'Invalid activation link.')
            return redirect('core:index')

class UsersResetPassword(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            context = {
               'user': user,
               'next': 'core:index',
               'uidb64': uidb64, 
               'token': token
            }
            return render(request, 'users/reset_password.html', context)
        else:
            messages.error(request, 'Invalid link.')
            return redirect('core:index')
        
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            messages.error(request, 'Error setting new password.')
            return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if password != confirm_password:
                messages.error(request, 'Your passwords do not match.')
                return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
            password_hash = make_password(password)
            user.password = password_hash
            user.save()
            messages.success(request, 'Your password has been reset.')
            return redirect('core:index')
        else:
            messages.error(request, 'Error setting new password.')
            return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
class UsersForgotPassword(View):
    def get(self, request):
        context = {
            'next': 'core:index'
        }
        return render(request, 'users/forgot_password.html', context)
    def post(self, request):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
          
            user.is_active = False
           
            user.save()           
            user.send_password_reset()
            
        except:
            pass

        messages.info(request, "An email has been sent.  If you don't receive the link, check your SPAM folder or verify the email address and try again.")    

        return redirect('core:index')

    
class UsersViewProfile(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            messages.error(request, "Cannot load profile.")
            return redirect('core:index')
       
        context = {
            'user': user,
       
        }
        return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def get_profile(request, pk):
    if request.htmx == False:
        return Http404
    try:
        user = User.objects.get(id= pk)
      
    except:
        messages.error(request, "Cannot load profile.")
        return redirect('core:index')
    
    
    context = {
        'user': user,
        'tab': 1
    }
    return render(request, 'users/partials/tab.html', context)

@login_required(login_url='login')
def change_password(request, pk):
    if request.htmx == False:
        return Http404
    
    try:
        user = User.objects.get(id= pk)
    except:
        messages.error(request, "Cannot load profile.")
        return render(request, 'users/partials/tab.html', {'user': None, 'tab': 99})
    context = {
        'user': user,
        'tab': 99
    }
    if request.method == "POST":
        print(request.POST)
        # check password with current password
        password = request.POST['password']
       
        try:
            print(user.password)
            password_match = check_password(password, user.password)
        except:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'users/partials/tab.html', context)
        if password_match == False:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'users/partials/tab.html', context)
        # check if new password matches confirm password
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'users/partials/tab.html', context)
        # check if the new password is valid before saving
        try:
            validate_password(new_password, user)
        except Exception as ex:
            for msg in ex.messages:
                messages.add_message(request, messages.ERROR, msg)
                return render(request, 'users/partials/tab.html', context)
        update_password = make_password(new_password)
        user.password = update_password
        user.save()
        messages.success(request, "Your password has been changed.")

        return render(request, 'users/partials/tab.html', context)
        

    
    return render(request, 'users/partials/tab.html', context)