# Generated by Django 4.2.7 on 2024-12-05 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0012_remove_monitorpolicy_query_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitorevent',
            name='monitor_instance',
        ),
        migrations.RemoveField(
            model_name='monitorevent',
            name='policy',
        ),
        migrations.DeleteModel(
            name='MonitorAlert',
        ),
        migrations.DeleteModel(
            name='MonitorEvent',
        ),
    ]