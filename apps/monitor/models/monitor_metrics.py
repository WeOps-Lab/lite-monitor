from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.monitor.models.monitor_object import MonitorObject


class MetricGroup(TimeInfo, MaintainerInfo):
    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='指标对象')
    name = models.CharField(max_length=100, verbose_name='指标分组名称')
    description = models.TextField(blank=True, null=True, verbose_name='指标分组描述')

    class Meta:
        verbose_name = '指标分组'
        verbose_name_plural = '指标分组'
        unique_together = ('monitor_object', 'name')


class Metric(TimeInfo, MaintainerInfo):

    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='指标对象')
    metric_group = models.ForeignKey(MetricGroup, on_delete=models.CASCADE, verbose_name='指标分组')
    name = models.CharField(max_length=100, verbose_name="指标名称")
    display_name = models.CharField(max_length=100, default="", verbose_name='指标展示名称')
    type = models.CharField(max_length=50, verbose_name='指标类型')
    query = models.TextField(default="", verbose_name='查询语句')
    unit = models.CharField(max_length=50, default="", verbose_name='指标单位')
    data_type = models.CharField(max_length=50, default="", verbose_name='数据类型')
    description = models.TextField(blank=True, null=True, verbose_name='指标描述')
    dimensions = models.JSONField(default=list, verbose_name='维度')

    class Meta:
        unique_together = ('monitor_object', 'name')
        verbose_name = '指标'
        verbose_name_plural = '指标'
