# Generated by Django 4.2.7 on 2024-12-23 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoralert',
            name='end_event_id',
        ),
        migrations.RemoveField(
            model_name='monitoralert',
            name='start_event_id',
        ),
    ]
