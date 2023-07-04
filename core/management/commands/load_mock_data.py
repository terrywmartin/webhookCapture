from django.core.management.base import BaseCommand
from django.conf import settings

import json
import os

from webhook.models import Payload, Webhook

class Command(BaseCommand):
    help = 'Loads mock data in database'

    def handle(self, *args, **kwargs):
        demo_key = settings.DEMO_WEBHOOK
        webhook = Webhook.objects.get(id=demo_key)
        data_files = ['MOCK_DATA_1','MOCK_DATA_2','MOCK_DATA_3','MOCK_DATA_4']
        payload_array = []
        for file in data_files:
            filepath = os.path.join(settings.BASE_DIR, 'core', 'data', file + '.json')
            with open(filepath, 'r') as f:
                data_array = json.load(f)
            for obj in data_array:
                payload_array.append(Payload(webhook=webhook, data=obj))

        Payload.objects.bulk_create(payload_array)
            
            