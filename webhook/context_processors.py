from .models import Webhook

def all_webhooks(request):
    if request.user.is_authenticated:
        return {
            'all_webhooks': Webhook.objects.filter(user=request.user).values('id', 'key','name')
        }
    else:
        return {
            'all_webhooks': None
        }