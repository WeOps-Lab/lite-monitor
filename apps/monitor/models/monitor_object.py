from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class MonitorObject(TimeInfo, MaintainerInfo):
    name = models.CharField(unique=True, max_length=100, verbose_name='监控对象')
    type = models.CharField(max_length=50, verbose_name='监控对象类型')
    description = models.TextField(blank=True, verbose_name='监控对象描述')

    class Meta:
        verbose_name = '监控对象'
        verbose_name_plural = '监控对象'


class MonitorInstance(TimeInfo, MaintainerInfo):
    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='监控对象')
    instance_id = models.CharField(db_index=True, max_length=100, verbose_name='监控对象实例id')
    organization = models.CharField(db_index=True, max_length=100, verbose_name='组织id')

    class Meta:
        verbose_name = '监控对象实例'
        verbose_name_plural = '监控对象实例'
        unique_together = ('monitor_object', 'instance_id', 'organization')


class MonitorInstanceGroupingRule(TimeInfo, MaintainerInfo):

    SELECT = 'select'
    CONDITION = 'condition'
    RULE_TYPE_CHOICES = (
        (SELECT, 'Select'),
        (CONDITION, 'Condition'),
    )

    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='监控对象')
    name = models.CharField(max_length=100, verbose_name='分组规则名称')
    type = models.CharField(max_length=30, choices=RULE_TYPE_CHOICES, verbose_name='分组规则类型')
    organizations = models.JSONField(default=list, verbose_name='所属组织')
    grouping_rules = models.JSONField(default=dict, verbose_name='分组规则详情')


    class Meta:
        verbose_name = '监控实例分组规则'
        verbose_name_plural = '监控实例分组规则'