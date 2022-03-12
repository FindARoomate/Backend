# Generated by Django 4.0.1 on 2022-02-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waitlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
