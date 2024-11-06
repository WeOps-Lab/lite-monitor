import logging

from celery import shared_task

from apps.monitor.models.monitor_object import MonitorInstanceGroupingRule, MonitorInstance
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI

logger = logging.getLogger("app")


@shared_task
def update_grouping_rule():
    logger.info("Start to update monitor instance grouping rule")
    RuleGrouping().update_grouping()
    logger.info("Finish to update monitor instance grouping rule")


class RuleGrouping:
    def __init__(self):
        self.rules = MonitorInstanceGroupingRule.objects.all()

    def get_asso_by_condition_rule(self, rule):
        """根据条件类型规则获取关联信息"""
        asso_list = []
        metrics = VictoriaMetricsAPI().query(rule.grouping_rules["query"])
        for metric_info in metrics.get("result", []):
            instance_id = metric_info["metric"].get("instance_id")
            if instance_id:
                asso_list.extend([(instance_id, i) for i in rule.organizations])
        return asso_list

    def get_asso_by_select_rule(self, rule):
        """根据选择类型规则获取关联信息"""
        asso_list = []
        for instance_id in rule.grouping_rules["instances"]:
            asso_list.extend([(instance_id, i) for i in rule.organizations])
        return asso_list


    def update_grouping(self):
        """更新监控实例分组"""
        monitor_inst_asso_set = set()
        for rule in self.rules:
            if rule.type == MonitorInstanceGroupingRule.CONDITION:
                asso_list = self.get_asso_by_condition_rule(rule)
            elif rule.type == MonitorInstanceGroupingRule.SELECT:
                asso_list = self.get_asso_by_select_rule(rule)
            else:
                continue
            for instance_id, organization in asso_list:
                monitor_inst_asso_set.add((rule.monitor_object_id, instance_id, organization))

        exist_instance_map = {(i.monitor_object_id, i.instance_id, i.organization): i.id for i in MonitorInstance.objects.all()}
        create_asso_set = monitor_inst_asso_set - set(exist_instance_map.keys())
        delete_asso_set = set(exist_instance_map.keys()) - monitor_inst_asso_set

        create_objs = [
            MonitorInstance(monitor_object_id=asso_tuple[0], instance_id=asso_tuple[1], organization=asso_tuple[2])
            for asso_tuple in create_asso_set
        ]
        if create_objs:
            MonitorInstance.objects.bulk_create(create_objs, batch_size=200)

        if delete_asso_set:
            delete_ids = [exist_instance_map[asso_tuple] for asso_tuple in delete_asso_set]
            MonitorInstance.objects.filter(id__in=delete_ids).delete()