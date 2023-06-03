from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('capture/<uuid:key>', views.capture_webhook, name='capture' )
]