from celery import shared_task
from captureWebhooks.celery import app

from .models import Payload

@shared_task
def clean_database():
    try:

        Payload.objects.all().delete()
    except:
        print('Error cleaning database')

@shared_task
def delete_payloads(pk):
    Payload.objects.filter(webhook__user_id = pk).delete()