# Generated by Django 4.2.7 on 2024-12-18 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0026_metricgroup_monitor_plugin'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AddField(
            model_name='metricgroup',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
    ]
