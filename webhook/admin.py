from django.contrib import admin

from .models import Webhook, Credentials, Payload

# Register your models here.
admin.site.register(Webhook)
admin.site.register(Credentials)
admin.site.register(Payload)