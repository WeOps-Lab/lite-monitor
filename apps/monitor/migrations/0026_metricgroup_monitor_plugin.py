# Generated by Django 4.2.7 on 2024-12-17 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0025_metric_is_pre_metricgroup_is_pre_alter_metric_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricgroup',
            name='monitor_plugin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorplugin', verbose_name='监控插件'),
        ),
    ]