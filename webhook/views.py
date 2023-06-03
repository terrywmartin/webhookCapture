from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

import uuid

from .models import Webhook, Credentials, Payload
from .forms import WebhookModelForm, CredentialModelForm
from .utils import create_jwt

# Create your views here.

class WebhookViewWebhooks(LoginRequiredMixin, View):
     def get(self, request):
          try:
               webhooks = Webhook.objects.filter(user__id=request.user.id)

          except:
               messages.error(request, "Cannot load webhooks.")
               webhooks = None
          
          context = {
               'webhooks': webhooks,
          }

          return render(request, 'webhook/view_webhooks.html', context)

          
     
class WebhookViewWebhook(LoginRequiredMixin, View):
     def get(self, request, pk):
          pass
     
class WebhookCreateWebhook(LoginRequiredMixin, View):
     def get(self, request):
          cred_form = CredentialModelForm()
          webhook_form = WebhookModelForm()

          context = {
               'cred_form': cred_form,
               'webhook_form': webhook_form
          }
          return render(request, 'webhook/create_webhook.html', context)
     def post(self, request):
          
          cred_form = CredentialModelForm(request.POST)
          if cred_form.is_valid():

               type = request.POST['type']
               name = request.POST['name']
               user = request.user
               username = ''
               password = ''
               token = ''

               if type == 'token':
                    token = create_jwt(name)

               cred = Credentials(type=type, token=token, username=username, password=password)
               cred.save()
               webhook = Webhook(name=name, user=user, key=uuid.uuid4(),credential=cred )     
               webhook.save()
               
               #return render(request, 'webhook/edit_webhook.html', context)
               return redirect('webhook:edit_webhook', pk=webhook.id)
     
class WebhookEditWebhook(LoginRequiredMixin, View):
     def get(self, request, pk):
          try:
               webhook = Webhook.objects.select_related('credential').get(id=pk)

          except:
               messages.error(request, "Can't load webhook.")

          cred_form = CredentialModelForm(instance=webhook.credential)
          context = {
               'webhook': webhook,
               'cred_form': cred_form,
               'token': webhook.credential.token,
               'key': webhook.key,
               'un': webhook.credential.username,
               'pw': webhook.credential.password
          }

          return render(request, 'webhook/edit_webhook.html', context)
     
     def post(self, request, pk):
          print(request.POST)
          print(pk)
          try:     
               webhook = Webhook.objects.get(id=pk, user=request.user)
               name = request.POST['name']
               type = request.POST['type']
               username = request.POST['username']
               password = request.POST['password']
               print(webhook)
               webhook.name = name 
               if webhook.credential.type != type:
                    if type == 'token':
                         token = create_jwt(name)
                         webhook.credential.type = 'token'
                         webhook.credential.token = token
               if type == 'basic':
                    print(username,password)
                    webhook.credential.username = username
                    webhook.credential.password = password
               print(webhook.credential.username)
               webhook.credential.type = type
               webhook.credential.save()
               webhook.save()
          except:
               messages.error(request, "Error saving webhook.")

          webhooks = Webhook.objects.filter(user=request.user)
          context = {
               'webhooks': webhooks
          }
          return render(request, 'webhook/view_webhooks.html', context)
     
class WebhookDeleteWebhook(LoginRequiredMixin, View):
     def delete(self, request, pk):
          if request.htmx == False:
            return Http404
          
          webhook = Webhook.objects.filter(id=pk, user = request.user)
          webhook.delete()

          webhooks = Webhook.objects.filter(user=request.user)
          context = {
               'webhooks': webhooks
          }
          return render(request, 'webhook/partials/webhooks.html')

class WebhookCapture(View):
    
     def get(self,request, key):
          
          payloads = Payload.objects.filter(webhook__key=key).values('id','data')
          
          for payload in payloads:
               payload['preview'] = str(payload['data'])[0:100] 
          
          context = {
               'key': key,
               'payloads': payloads,
          }

          return render(request, 'webhook/view.html', context)
    
    
@login_required(login_url='login') 
def get_payloads(request, key):
    if request.htmx == False:
            return Http404
    
    payloads = Payload.objects.filter(webhook__key=key).values('id','data')
    
    for payload in payloads:
            payload['preview'] = str(payload['data'])[0:100] 

    context = {
        'key': key,
        'payloads': payloads
    }

    return render(request, 'webhook/partials/payloads.html', context)

@login_required(login_url='login')
def get_payload(request, pk):
    if request.htmx == False:
            return Http404

    try:
        payload = Payload.objects.get(id=pk)

    except:
        messages.error(request, "Error getting data.") 
        context = {
             'data': None
        }
        return render(request,'webhook/partials/payload.html', context)
    
   
    context = {
         'data': payload.data
    }

    return render(request, 'webhook/partials/payload.html', context)

@login_required(login_url='login')
def create_token(request, name):
    if request.htmx == False:
            return Http404     
    try:
        token = create_jwt(name)

    except:
        messages.error(request, "Error getting data.") 
        context = {
             'token': ''
        }
        return render(request,'webhook/partials/token.html', context)
    
    print(f'passing token: {token}')
   
    context = {
         'token': str(token)
    }

    return render(request, 'webhook/partials/token.html', context)

@login_required(login_url='login')
def create_key(request):
     if request.htmx == False:
            return Http404

     key = uuid.uuid4()
   
     context = {
          'key': key
     }

     return render(request, 'webhook/partials/key.html', context)