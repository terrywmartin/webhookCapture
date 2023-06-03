from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from django.shortcuts import get_object_or_404
from django.http import Http404

import base64

from webhook.models import Webhook, Credentials, Payload

@api_view(['POST'])
@authentication_classes([BasicAuthentication,TokenAuthentication])
def capture_webhook(request, key):
    try:
        webhook = get_object_or_404(Webhook, key=key)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header != None:

            auth_type=str(auth_header).split(' ')[0]
            creds = str(auth_header).split(' ')[1]

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
        #webhook = Webhook(key=key)
        #webhook.save()
        payload = Payload(webhook=webhook, data=request.data)
        payload.save()
    except:
        resp = { 'status': 404 }
        return Response(resp, status=status.HTTP_404_NOT_FOUND)

    resp = { 'status': 200 }
    return Response(resp, status=status.HTTP_200_OK)
    
