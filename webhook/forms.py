from django.forms import ModelForm

from .models import Webhook, Credentials

class WebhookModelForm(ModelForm):
    class Meta:
        model = Webhook
        fields = [ 'name' ]

    def __init__(self, *args, **kwargs):
        
        super(WebhookModelForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class CredentialModelForm(ModelForm):
    class Meta:
        model = Credentials
        fields = [ 'type' ]

    def __init__(self, *args, **kwargs):
        
        super(CredentialModelForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})