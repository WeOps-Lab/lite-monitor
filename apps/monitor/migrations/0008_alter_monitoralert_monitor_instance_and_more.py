# Generated by Django 4.2.7 on 2024-11-29 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_monitoralert_content_monitorevent_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoralert',
            name='monitor_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.monitorinstance', verbose_name='监控实例'),
        ),
        migrations.AlterField(
            model_name='monitoralert',
            name='policy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.monitorpolicy', verbose_name='监控策略'),
        ),
        migrations.AlterField(
            model_name='monitorevent',
            name='monitor_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.monitorinstance', verbose_name='监控实例'),
        ),
        migrations.AlterField(
            model_name='monitorevent',
            name='policy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='monitor.monitorpolicy', verbose_name='监控策略'),
        ),
    ]
