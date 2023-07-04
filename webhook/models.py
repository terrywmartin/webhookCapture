from django.db import models


import uuid

from users.models import User

# Create your models here.

class Credentials(models.Model):
    CRED_TYPE = (
        ('token', 'Token'),
        ('basic', 'Basic Auth'),
    )

    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    token = models.TextField(null=True,blank=True)   
    username = models.CharField(max_length=100,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    type = models.CharField(choices=CRED_TYPE,max_length=100, default='token')

    
class Webhook(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    name = models.CharField(max_length=100,null=False,blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    key = models.UUIDField(default=uuid.uuid4,null=True,blank=True )
    credential = models.ForeignKey(Credentials,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created_at']

class Payload(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    webhook = models.ForeignKey(Webhook,null=True,blank=True,on_delete=models.CASCADE,related_name='webhook')
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.data)[1:50]