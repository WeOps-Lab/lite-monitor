# Generated by Django 4.2.7 on 2024-12-06 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0016_monitorpolicy_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorpolicy',
            name='last_run_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='最后一次执行时间'),
        ),
    ]
