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

from .tasks import handle_payload

@api_view(['POST'])
# @authentication_classes([BasicAuthentication,TokenAuthentication])
def capture_webhook(request, key):
    try:
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header == None:
           raise Http404
        handle_payload(key, auth_header, request.data)
    except:
        resp = { 'status': 404 }
        return Response(resp, status=status.HTTP_404_NOT_FOUND)

    resp = { 'status': 200 }
    return Response(resp, status=status.HTTP_200_OK)
    
