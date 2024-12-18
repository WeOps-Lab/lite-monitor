# Generated by Django 4.2.7 on 2024-12-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0027_metric_sort_order_metricgroup_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorinstance',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='监控对象实例ID'),
        ),
        migrations.AlterField(
            model_name='monitorinstance',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=200, verbose_name='监控对象实例名称'),
        ),
    ]
