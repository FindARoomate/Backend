# Generated by Django 4.0.1 on 2022-05-31 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_connection_roomate_request_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='user',
        ),
        migrations.AddField(
            model_name='connection',
            name='reciever',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='connection',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
