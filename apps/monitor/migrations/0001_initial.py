# Generated by Django 4.2.7 on 2024-11-22 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, verbose_name='指标名称')),
                ('display_name', models.CharField(default='', max_length=100, verbose_name='指标展示名称')),
                ('type', models.CharField(max_length=50, verbose_name='指标类型')),
                ('query', models.TextField(default='', verbose_name='查询语句')),
                ('unit', models.CharField(default='', max_length=50, verbose_name='指标单位')),
                ('data_type', models.CharField(default='', max_length=50, verbose_name='数据类型')),
                ('description', models.TextField(blank=True, null=True, verbose_name='指标描述')),
                ('dimensions', models.JSONField(default=list, verbose_name='维度')),
            ],
            options={
                'verbose_name': '指标',
                'verbose_name_plural': '指标',
            },
        ),
        migrations.CreateModel(
            name='MonitorObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='监控对象')),
                ('type', models.CharField(max_length=50, verbose_name='监控对象类型')),
                ('description', models.TextField(blank=True, verbose_name='监控对象描述')),
            ],
            options={
                'verbose_name': '监控对象',
                'verbose_name_plural': '监控对象',
            },
        ),
        migrations.CreateModel(
            name='MonitorPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('query', models.TextField(default='', verbose_name='查询语句')),
                ('name', models.CharField(max_length=100, verbose_name='监控策略名称')),
                ('organizations', models.JSONField(default=list, verbose_name='所属组织')),
                ('source', models.JSONField(default=dict, verbose_name='策略适用的资源')),
                ('schedule', models.JSONField(default=dict, verbose_name='策略执行周期(crontab格式)')),
                ('period', models.IntegerField(verbose_name='每次监控检测的数据周期(秒)')),
                ('algorithm', models.CharField(choices=[('sum', 'SUM'), ('avg', 'AVG'), ('max', 'MAX'), ('min', 'MIN'), ('new', 'NEW')], max_length=10, verbose_name='聚合算法')),
                ('threshold', models.JSONField(default=list, verbose_name='阈值')),
                ('recovery_condition', models.SmallIntegerField(default=1, verbose_name='多少周期不满足阈值自动恢复')),
                ('no_data_alert', models.SmallIntegerField(default=1, verbose_name='连续多少周期无数据, 生成告警')),
                ('notice', models.BooleanField(default=True, verbose_name='是否通知')),
                ('notice_type', models.CharField(choices=[('email', 'Email'), ('wechat', 'Wechat'), ('sms', 'SMS')], default='email', max_length=10, verbose_name='通知方式')),
                ('notice_users', models.JSONField(default=list, verbose_name='通知人')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.metric', verbose_name='监控指标')),
                ('monitor_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorobject', verbose_name='监控对象')),
            ],
            options={
                'verbose_name': '监控策略',
                'verbose_name_plural': '监控策略',
            },
        ),
        migrations.CreateModel(
            name='MonitorInstanceGroupingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, verbose_name='分组规则名称')),
                ('type', models.CharField(choices=[('select', 'Select'), ('condition', 'Condition')], max_length=30, verbose_name='分组规则类型')),
                ('organizations', models.JSONField(default=list, verbose_name='所属组织')),
                ('grouping_rules', models.JSONField(default=dict, verbose_name='分组规则详情')),
                ('monitor_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorobject', verbose_name='监控对象')),
            ],
            options={
                'verbose_name': '监控实例分组规则',
                'verbose_name_plural': '监控实例分组规则',
            },
        ),
        migrations.CreateModel(
            name='MonitorInstance',
            fields=[
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='监控对象实例ID')),
                ('name', models.CharField(db_index=True, default='', max_length=100, verbose_name='监控对象实例名称')),
                ('interval', models.IntegerField(default=10, verbose_name='监控实例采集间隔(s)')),
                ('agent_id', models.CharField(default='', max_length=100, verbose_name='Agent ID')),
                ('auto', models.BooleanField(default=False, verbose_name='是否自动发现')),
                ('monitor_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorobject', verbose_name='监控对象')),
            ],
            options={
                'verbose_name': '监控对象实例',
                'verbose_name_plural': '监控对象实例',
                'unique_together': {('monitor_object', 'name')},
            },
        ),
        migrations.CreateModel(
            name='MonitorEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='事件生成时间')),
                ('value', models.FloatField(verbose_name='事件值')),
                ('level', models.CharField(choices=[('no_data', 'No Data'), ('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('critical', 'Critical')], max_length=20, verbose_name='事件级别')),
                ('notice_result', models.BooleanField(default=True, verbose_name='通知结果')),
                ('monitor_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorinstance', verbose_name='监控实例')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorpolicy', verbose_name='监控策略')),
            ],
        ),
        migrations.CreateModel(
            name='MonitorAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('alert_type', models.CharField(choices=[('alert', 'Alert'), ('no_data', 'No Data')], default='alert', max_length=50, verbose_name='告警类型')),
                ('status', models.CharField(choices=[('new', 'New'), ('closed', 'Closed'), ('recovered', 'Recovered')], db_index=True, default='new', max_length=20, verbose_name='告警状态')),
                ('start_event_id', models.IntegerField(blank=True, null=True, verbose_name='开始事件ID')),
                ('start_event_time', models.DateTimeField(blank=True, null=True, verbose_name='开始事件时间')),
                ('end_event_id', models.IntegerField(blank=True, null=True, verbose_name='结束事件ID')),
                ('end_event_time', models.DateTimeField(blank=True, null=True, verbose_name='结束事件时间')),
                ('operator', models.CharField(max_length=50, verbose_name='告警处理人')),
                ('monitor_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorinstance', verbose_name='监控实例')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorpolicy', verbose_name='监控策略')),
            ],
            options={
                'verbose_name': '监控告警',
                'verbose_name_plural': '监控告警',
            },
        ),
        migrations.CreateModel(
            name='MetricGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=100, verbose_name='指标分组名称')),
                ('description', models.TextField(blank=True, null=True, verbose_name='指标分组描述')),
                ('monitor_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorobject', verbose_name='指标对象')),
            ],
            options={
                'verbose_name': '指标分组',
                'verbose_name_plural': '指标分组',
                'unique_together': {('monitor_object', 'name')},
            },
        ),
        migrations.AddField(
            model_name='metric',
            name='metric_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.metricgroup', verbose_name='指标分组'),
        ),
        migrations.AddField(
            model_name='metric',
            name='monitor_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorobject', verbose_name='指标对象'),
        ),
        migrations.CreateModel(
            name='MonitorInstanceOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='更新者')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('organization', models.CharField(max_length=100, verbose_name='组织id')),
                ('monitor_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorinstance', verbose_name='监控对象实例')),
            ],
            options={
                'verbose_name': '监控对象实例组织',
                'verbose_name_plural': '监控对象实例组织',
                'unique_together': {('monitor_instance', 'organization')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='metric',
            unique_together={('monitor_object', 'name')},
        ),
    ]
