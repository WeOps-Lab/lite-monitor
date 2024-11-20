import logging

from celery.app import shared_task

from apps.monitor.constants import POLICY_METHODS, THRESHOLD_METHODS
from apps.monitor.models import MonitorPolicy, MonitorInstanceOrganization, MonitorAlert, MonitorEvent
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


logger = logging.getLogger("app")


@shared_task
def scan_policy():
    """扫描监控策略"""
    logger.info("Start to update monitor instance grouping rule")
    policy_objs = MonitorPolicy.objects.all()
    for policy in policy_objs:
        MonitorPolicyScan(policy).run()
    logger.info("Finish to update monitor instance grouping rule")


class MonitorPolicyScan:
    def __init__(self, policy):
        self.policy = policy

    def get_instances(self):
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
        return instance_list

    def query_metrics(self):
        """查询指标"""
        instances = self.get_instances()
        query = self.policy.query
        instances_str = "|".join(instances)
        query.replace("__labels__", f"instance_id=~'{instances_str}'")
        metrics = VictoriaMetricsAPI().query(query)
        return metrics

    def metric_aggregation(self, metrics):
        """指标聚合"""
        method = POLICY_METHODS.get(self.policy.algorithm)
        if not method:
            raise ValueError("Invalid algorithm")
        metrics_map = {}
        for metric_info in metrics.get("result", []):
            instance_id = metric_info["metric"].get("instance_id")
            if instance_id not in metrics_map:
                metrics_map[instance_id] = []
            metrics_map[instance_id].append(metric_info["value"][1])

        result = {instance_id: method(values) for instance_id, values in metrics_map.items()}
        return result

    def compare(self, aggregation_result):
        """对比结果, 生成告警事件"""
        compare_result = []

        for instance_id, value in aggregation_result.items():

            event = None
            for threshold_info in self.policy.threshold:
                method = THRESHOLD_METHODS.get(threshold_info["method"])
                if not method:
                    raise ValueError("Invalid threshold method")
                if method(value, threshold_info["value"]):
                    event = {
                        "instance_id": instance_id,
                        "value": value,
                        "level": threshold_info["level"],
                    }
                    break

            if not event:
                event = {
                    "instance_id": instance_id,
                    "value": value,
                    "level": "info",
                }

            compare_result.append(event)

        return compare_result

    def event_handling(self, events: list):
        """事件处理"""
        alert_instance_map = self.create_or_get_alert(events)
        for event in events:
            event.update(monitor_alert_id=alert_instance_map[event["instance_id"]])

        # 创建告警事件
        self.create_event(events)

        # 处理告警恢复
        self.recovery(events)

    def create_or_get_alert(self, events):
        """创建或获取告警"""
        new_event_instance_ids = [event["instance_id"] for event in events]
        alert_objs = MonitorAlert.objects.filter(
            policy_id=self.policy.id, status="new",monitor_instance_id__in=new_event_instance_ids)
        alert_instance_map = {alert.monitor_instance_id: alert.id for alert in alert_objs}
        new_alerts = set(new_event_instance_ids) - set(alert_instance_map.keys())
        new_alert_creates = [
            MonitorAlert(policy_id=self.policy.id, monitor_instance_id=instance_id, status="new")
            for instance_id in new_alerts
        ]
        new_alert_objs = MonitorAlert.objects.bulk_create(new_alert_creates, batch_size=200)
        for alert in new_alert_objs:
            alert_instance_map[alert.monitor_instance_id] = alert.id
        return alert_instance_map

    def create_event(self, events):
        """创建事件"""
        new_event_creates = [
            MonitorEvent(
                monitor_alert_id=event["monitor_alert_id"],
                value=event["value"],
                level=event["level"],
                notice_result=True
            )
            for event in events
        ]
        MonitorEvent.objects.bulk_create(new_event_creates, batch_size=200)

    def recovery(self, events):
        """告警恢复"""
        need_check_events = [event for event in events if event["level"] == "info"]

        recovery_condition = self.policy.recovery_condition

        alerts = MonitorAlert.objects.filter(
            id__in=[event["monitor_alert_id"] for event in need_check_events]).prefetch_related("monitorevent_set")

        recovery_alerts = []

        for alert in alerts:
            event_objs = alert.monitorevent_set.all().order_by("-created_at")
            count = 0
            for event_obj in event_objs:
                if event_obj.level != "info":
                    break
                count += 1
            if count >= recovery_condition:
                alert.status = "recovered"
                recovery_alerts.append(alert)

        MonitorAlert.objects.bulk_update(recovery_alerts, ["status"], batch_size=200)

    def notice(self, events):
        """通知"""
        # todo 告警通知
        for event in events:
            logger.info(f"Instance {event['instance_id']} has a new event, value is {event['value']}")
        pass

    def run(self):
        """运行"""
        metrics = self.query_metrics()
        aggregation_result = self.metric_aggregation(metrics)
        events = self.compare(aggregation_result)
        self.event_handling(events)
