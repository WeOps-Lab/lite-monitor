# Generated by Django 4.2.7 on 2024-12-17 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0022_remove_metric_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricgroup',
            name='display_name',
            field=models.CharField(default='', max_length=100, verbose_name='指标分组展示名称'),
        ),
    ]
