from celery import shared_task

from django.shortcuts import get_object_or_404
from django.http import Http404

import base64

from webhook.models import Webhook, Payload

@shared_task
def handle_payload(key, auth_header, data):
    try:
       
        if auth_header != None:
            auth_type=str(auth_header).split(' ')[0]
            creds = str(auth_header).split(' ')[1]
            webhook = get_object_or_404(Webhook, key=key)
            if auth_type == 'Basic':
                creds_decoded = base64.b64decode(creds).decode("ascii")
                username = creds_decoded.split(':')[0]
                password = creds_decoded.split(':')[1]                
                if webhook.credential.type != 'basic':
                    raise Http404
                if webhook.credential.username != username or webhook.credential.password != password:
                    raise Http404                
            elif auth_type == 'Bearer': 
                token = creds
                if webhook.credential.type != 'token':
                    raise Http404
                
                if webhook.credential.token != token:
                    raise Http404
                
            else:
                raise Http404
        else:
            raise Http404
        payload = Payload(webhook=webhook, data=data)
        payload.save()
    except Http404:
        # add logging
        # ignore for now
        pass
