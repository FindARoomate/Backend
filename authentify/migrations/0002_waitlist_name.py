# Generated by Django 4.0.1 on 2022-04-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitlist',
            name='name',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
