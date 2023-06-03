from django.contrib import admin
from django.urls import path

from . import views

app_name = 'webhook'

urlpatterns = [
    path('capture/<uuid:key>/', views.WebhookCapture.as_view(), name='capture'),
    path('payloads/<uuid:key>', views.get_payloads, name='get_payloads'),
    path('payload/<uuid:pk>', views.get_payload, name='get_payload'),

    path('', views.WebhookViewWebhooks.as_view(), name='view_webhooks'),
    #path('<uuid:pk>/', views.WebhookViewWebhook.as_view(), name='view_webhook'),
    path('<uuid:key>/', views.WebhookCapture.as_view(), name='view_webhook'),
    path('<uuid:pk>/edit/', views.WebhookEditWebhook.as_view(), name='edit_webhook'),
    path('<uuid:pk>/delete/', views.WebhookDeleteWebhook.as_view(), name='delete_webhook'),
    path('create/', views.WebhookCreateWebhook.as_view(), name='create_webhook'),
    path('create_token/<str:name>', views.create_token, name='create_token'),
    path('create_key/', views.create_key, name='create_key'),





]
