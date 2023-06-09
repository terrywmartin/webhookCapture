# Generated by Django 4.2.1 on 2023-06-05 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.TextField(blank=True, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('token', 'Token'), ('basic', 'Basic Auth')], default='token', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('key', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('credential', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webhook.credentials')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Payload',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('data', models.JSONField(blank=True, null=True)),
                ('webhook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webhook', to='webhook.webhook')),
            ],
        ),
    ]
