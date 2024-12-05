import logging

from celery.app import shared_task
from datetime import datetime, timezone

from apps.monitor.constants import POLICY_METHODS, THRESHOLD_METHODS, LEVEL_WEIGHT, MONITOR_OBJS
from apps.monitor.models import MonitorPolicy, MonitorInstanceOrganization, MonitorAlert, MonitorEvent, MonitorInstance
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


logger = logging.getLogger("app")


@shared_task
def scan_policy_task(policy_id):
    """扫描监控策略"""
    logger.info("start to update monitor instance grouping rule")
    policy_obj = MonitorPolicy.objects.filter(id=policy_id).select_related("metric", "monitor_object").first()
    if policy_obj:
        MonitorPolicyScan(policy_obj).run()
    else:
        logger.warning(f"No MonitorPolicy found with id {policy_id}")
    logger.info("end to update monitor instance grouping rule")

class MonitorPolicyScan:
    def __init__(self, policy):
        self.policy = policy
        self.instances_map = self.instances_map()
        self.active_alerts = self.get_active_alerts()
        self.instance_id_key = None

    def get_active_alerts(self):
        """获取策略的活动告警"""
        return MonitorAlert.objects.filter(policy_id=self.policy.id, status="new")

    def instances_map(self):
        """获取策略适用的实例"""
        source_type, source_values = self.policy.source["type"], self.policy.source["values"]
        if source_type == "instance":
            instance_list = source_values
        elif source_type == "organization":
            instance_list = list(MonitorInstanceOrganization.objects.filter(organization__in=source_values).values_list(
                "monitor_instance_id", flat=True
            ))
        else:
            instance_list = []
        objs = MonitorInstance.objects.filter(id__in=instance_list)
        return {i.id: i.name for i in objs}

    def format_to_vm_filter(self, conditions):
        """
        将纬度条件格式化为 VictoriaMetrics 的标准语法。

        Args:
            conditions (list): 包含过滤条件的字典列表，每个字典格式为：
                {"name": <纬度名称>, "value": <值>, "method": <运算符>}

        Returns:
            str: 格式化后的 VictoriaMetrics 过滤条件语法。
        """
        vm_filters = []
        for condition in conditions:
            name = condition.get("name")
            value = condition.get("value")
            method = condition.get("method")
            vm_filters.append(f'{name}{method}"{value}"')

        # 使用逗号连接多个条件
        return ",".join(vm_filters)

    def query_metrics(self):
        """查询指标"""
        step = int(self.policy.period / 10)
        end_timestamp = int(datetime.now(timezone.utc).timestamp())
        start_timestamp = end_timestamp - self.policy.period
        query = self.policy.metric.query
        instances_str = "|".join(self.instances_map.keys())
        instance_str = f"instance_id=~'{instances_str}'," if instances_str else ""
        vm_filter_str = self.format_to_vm_filter(self.policy.filter)
        vm_filter_str = f"{vm_filter_str}" if vm_filter_str else ""
        label_str = f"{instance_str}{vm_filter_str}"
        query = query.replace("__$labels__", label_str)
        metrics = VictoriaMetricsAPI().query_range(query, start_timestamp, end_timestamp, step)
        return metrics

    def set_monitor_obj_instance_key(self):
        """获取监控对象实例key"""
        for monitor_obj in MONITOR_OBJS:
            if monitor_obj["name"] == self.policy.monitor_object.name:
                self.instance_id_key= monitor_obj["instance_id_key"]
                break
        if not self.instance_id_key:
            raise ValueError("invalid monitor object instance key")

    def metric_aggregation(self, metrics):
        """指标聚合"""
        method = POLICY_METHODS.get(self.policy.algorithm)
        if not method:
            raise ValueError("invalid policy method")
        metrics_map = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = metric_info["metric"].get(self.instance_id_key)
            if instance_id not in metrics_map:
                metrics_map[instance_id] = []
            for value in metric_info["values"]:
                metrics_map[instance_id].append(float(value[1]))
        result = {instance_id: method(values) for instance_id, values in metrics_map.items()}
        return result

    def compare_event(self, aggregation_result):
        """比较事件"""
        compare_result = []

        # 计算无数据事件
        for instance_id in self.instances_map.keys():
            if instance_id not in aggregation_result:
                compare_result.append({
                    "instance_id": instance_id,
                    "value": None,
                    "level": "no_data",
                    "content": "no data",
                })

        # 计算告警事件
        for instance_id, value in aggregation_result.items():

            event = None
            for threshold_info in self.policy.threshold:
                method = THRESHOLD_METHODS.get(threshold_info["method"])
                if not method:
                    raise ValueError("invalid threshold method")
                if method(value, threshold_info["value"]):
                    event = {
                        "instance_id": instance_id,
                        "value": value,
                        "level": threshold_info["level"],
                        "content": f'{self.policy.monitor_object.type}-{self.policy.monitor_object.name} {self.instances_map.get(instance_id, "")} {self.policy.metric.name} {threshold_info["method"]} {threshold_info["value"]}',
                    }
                    break

            # 未触发阈值的事件
            if not event:
                event = {
                    "instance_id": instance_id,
                    "value": value,
                    "level": "info",
                    "content": "",
                }

            compare_result.append(event)

        return compare_result

    def create_event(self, events):
        """创建事件"""
        new_event_creates = [
            MonitorEvent(
                policy_id=self.policy.id,
                monitor_instance_id=event["instance_id"],
                value=event["value"],
                level=event["level"],
                content=event["content"],
                notice_result=True,
            )
            for event in events
        ]
        event_objs = MonitorEvent.objects.bulk_create(new_event_creates, batch_size=200)
        return event_objs

    def notice(self, events):
        """通知"""
        # todo 告警通知
        for event in events:
            logger.info(f"to {self.policy.notice_users}，instance {event['instance_id']} has a new event, value is {event['value']}")

    def recovery_alert(self, event_objs):
        """告警恢复处理"""
        if self.policy.recovery_condition <= 0:
            return
        event_objs_map = {event.monitor_instance_id: event for event in event_objs}
        recovery_alerts, alert_level_updates = [], []
        for alert in self.active_alerts:
            event_obj = event_objs_map.get(alert.monitor_instance_id)
            if alert.alert_type == "no_data":
                # 无数据告警恢复
                if event_obj.level != "no_data":
                    alert.status = "recovered"
                    alert.end_event_id = event_obj.id
                    alert.end_event_time = event_obj.created_at
                    recovery_alerts.append(alert)
            else:
                # 正常告警恢复
                if event_obj.level == "info":
                    events = MonitorEvent.objects.filter(
                        policy_id=self.policy.id,
                        monitor_instance_id=event_obj.monitor_instance_id,
                    ).order_by("-created_at")[:self.policy.recovery_condition]
                    if all(event.level == "info" for event in events):
                        alert.status = "recovered"
                        alert.end_event_id = event_obj.id
                        alert.end_event_time = event_obj.created_at
                        recovery_alerts.append(alert)
                else:
                    # 告警等级升级
                    new_level = event_obj.level
                    old_level = alert.level
                    if LEVEL_WEIGHT.get(new_level) > LEVEL_WEIGHT.get(old_level):
                        alert.level = new_level
                        alert.value = event_obj.value
                        alert.content = event_obj.content
                        alert_level_updates.append(alert)
        if alert_level_updates:
            MonitorAlert.objects.bulk_update(alert_level_updates, ["level"], batch_size=200)
        if recovery_alerts:
            MonitorAlert.objects.bulk_update(recovery_alerts, ["status", "end_event_id", "end_event_time"], batch_size=200)

    def create_alert(self, event_objs):
        """告警生成处理"""
        no_data_events, alert_events = [], []
        for event_obj in event_objs:
            if event_obj.level == "info":
                continue
            if event_obj.level == "no_data":
                if self.policy.no_data_alert <= 0:
                    continue
                no_data_events.append(event_obj)
            else:
                alert_events.append(event_obj)

        # 正常告警
        alert_objs = [
            MonitorAlert(
                policy_id=self.policy.id,
                monitor_instance_id=event_obj.monitor_instance_id,
                alert_type="alert",
                level=event_obj.level,
                value=event_obj.value,
                content=event_obj.content,
                status="new",
                start_event_id=event_obj.id,
                start_event_time=event_obj.created_at,
                operator="system",
            )
            for event_obj in alert_events
        ]

        # 无数据告警
        for event_obj in no_data_events:
            events = MonitorEvent.objects.filter(
                policy_id=self.policy.id,
                monitor_instance_id=event_obj.monitor_instance_id,
            ).order_by("-created_at")[:self.policy.no_data_alert]
            if all(event.level == "no_data" for event in events):
                alert_objs.append(
                    MonitorAlert(
                        policy_id=self.policy.id,
                        monitor_instance_id=event_obj.monitor_instance_id,
                        alert_type="no_data",
                        level=self.policy.no_data_level,
                        value=None,
                        content="no data",
                        status="new",
                        start_event_id=event_obj.id,
                        start_event_time=event_obj.created_at,
                        operator="system",
                    )
                )
        MonitorAlert.objects.bulk_create(alert_objs, batch_size=200)

    def alert_handling(self, event_objs):
        """告警处理"""

        active_alert_map = {alert.monitor_instance_id for alert in self.active_alerts}
        recovery_alert_events, create_alert_events = [], []
        for event_obj in event_objs:
            if event_obj.monitor_instance_id in active_alert_map:
                recovery_alert_events.append(event_obj)
            else:
                create_alert_events.append(event_obj)

        # 告警恢复处理
        self.recovery_alert(recovery_alert_events)

        # 告警生成处理
        self.create_alert(create_alert_events)

    def run(self):
        """运行"""
        self.set_monitor_obj_instance_key()
        metrics = self.query_metrics()
        aggregation_result = self.metric_aggregation(metrics)
        events = self.compare_event(aggregation_result)
        event_objs = self.create_event(events)
        self.alert_handling(event_objs)
