# Generated by Django 4.2.7 on 2024-11-27 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_alter_monitorinstance_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoralert',
            name='level',
            field=models.CharField(default='', max_length=20, verbose_name='告警级别'),
        ),
    ]
