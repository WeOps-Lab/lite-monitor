# Generated by Django 4.2.7 on 2024-12-06 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0015_monitorpolicy_group_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorpolicy',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='是否启用'),
        ),
    ]
