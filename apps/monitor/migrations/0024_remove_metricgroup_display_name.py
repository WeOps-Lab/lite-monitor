# Generated by Django 4.2.7 on 2024-12-17 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0023_metricgroup_display_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricgroup',
            name='display_name',
        ),
    ]
