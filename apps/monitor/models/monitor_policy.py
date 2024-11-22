from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.monitor.models.monitor_metrics import Metric
from apps.monitor.models.monitor_object import MonitorObject, MonitorInstance


class MonitorPolicy(TimeInfo, MaintainerInfo):
    ALGORITHM_CHOICES = [('sum', 'SUM'), ('avg', 'AVG'), ('max', 'MAX'), ('min', 'MIN'), ('new', 'NEW')]
    NOTICE_TYPE_CHOICES = [('email', 'Email'), ('wechat', 'Wechat'), ('sms', 'SMS')]

    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='监控对象')
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, verbose_name='监控指标')
    query = models.TextField(default="", verbose_name='查询语句')
    name = models.CharField(max_length=100, verbose_name='监控策略名称')
    organizations = models.JSONField(default=list, verbose_name='所属组织')
    source = models.JSONField(default=dict, verbose_name="策略适用的资源")
    schedule = models.JSONField(default=dict, verbose_name="策略执行周期(crontab格式)")
    period = models.IntegerField(verbose_name="每次监控检测的数据周期(秒)")
    algorithm = models.CharField(max_length=10, choices=ALGORITHM_CHOICES, verbose_name="聚合算法")
    threshold = models.JSONField(default=list, verbose_name="阈值")

    recovery_condition = models.SmallIntegerField(default=1, verbose_name="多少周期不满足阈值自动恢复")
    no_data_alert = models.SmallIntegerField(default=1, verbose_name="连续多少周期无数据, 生成告警")

    notice = models.BooleanField(default=True, verbose_name="是否通知")
    notice_type = models.CharField(max_length=10, default="email", choices=NOTICE_TYPE_CHOICES, verbose_name="通知方式")
    notice_users = models.JSONField(default=list, verbose_name="通知人")

    class Meta:
        verbose_name = '监控策略'
        verbose_name_plural = '监控策略'


class MonitorEvent(models.Model):
    LEVEL_CHOICES = [("no_data", "No Data"), ('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('critical', 'Critical')]

    policy = models.ForeignKey(MonitorPolicy, on_delete=models.CASCADE, verbose_name='监控策略')
    monitor_instance = models.ForeignKey(MonitorInstance, on_delete=models.CASCADE, verbose_name='监控实例')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="事件生成时间" )
    value = models.FloatField(verbose_name='事件值')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='事件级别')
    notice_result = models.BooleanField(default=True, verbose_name='通知结果')


class MonitorAlert(TimeInfo):
    STATUS_CHOICES = [('new', 'New'), ('closed', 'Closed'), ('recovered', 'Recovered')]
    ALERT_TYPE_CHOICES = [('alert', 'Alert'), ('no_data', 'No Data')]

    policy = models.ForeignKey(MonitorPolicy, on_delete=models.CASCADE, verbose_name='监控策略')
    monitor_instance = models.ForeignKey(MonitorInstance, on_delete=models.CASCADE, verbose_name='监控实例')
    alert_type = models.CharField(default="alert", choices=ALERT_TYPE_CHOICES, max_length=50, verbose_name='告警类型')
    status = models.CharField(db_index=True, max_length=20, default="new", choices=STATUS_CHOICES, verbose_name='告警状态')
    start_event_id = models.IntegerField(blank=True, null=True, verbose_name='开始事件ID')
    start_event_time = models.DateTimeField(blank=True, null=True, verbose_name='开始事件时间')
    end_event_id = models.IntegerField(blank=True, null=True, verbose_name='结束事件ID')
    end_event_time = models.DateTimeField(blank=True, null=True, verbose_name='结束事件时间')
    operator = models.CharField(max_length=50, verbose_name='告警处理人')

    class Meta:
        verbose_name = '监控告警'
        verbose_name_plural = '监控告警'