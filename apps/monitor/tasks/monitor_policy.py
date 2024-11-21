import logging

from celery.app import shared_task
from datetime import datetime, timezone

from apps.monitor.constants import POLICY_METHODS, THRESHOLD_METHODS
from apps.monitor.models import MonitorPolicy, MonitorInstanceOrganization, MonitorAlert, MonitorEvent
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


logger = logging.getLogger("app")


@shared_task
def scan_policy_task(policy_id):
    """扫描监控策略"""
    logger.info("start to update monitor instance grouping rule")
    policy_obj = MonitorPolicy.objects.get(id=policy_id)
    MonitorPolicyScan(policy_obj).run()
    logger.info("finish to update monitor instance grouping rule")


class MonitorPolicyScan:
    def __init__(self, policy):
        self.policy = policy
        self.instances = self.get_instances()
        self.active_alerts = self.get_active_alerts()

    def get_active_alerts(self):
        """获取策略的活动告警"""
        return MonitorAlert.objects.filter(policy_id=self.policy.id, status="new")

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
        step = int(self.policy.period / 10)
        end_timestamp = int(datetime.now(timezone.utc).timestamp())
        start_timestamp = end_timestamp - self.policy.period
        query = self.policy.query
        instances_str = "|".join(self.instances)
        query.replace("__labels__", f"instance_id=~'{instances_str}'")
        metrics = VictoriaMetricsAPI().query_range(query, start_timestamp, end_timestamp, step)
        return metrics

    def metric_aggregation(self, metrics):
        """指标聚合"""
        method = POLICY_METHODS.get(self.policy.algorithm)
        if not method:
            raise ValueError("invalid policy method")
        metrics_map = {}
        for metric_info in metrics.get("result", []):
            instance_id = metric_info["metric"].get("instance_id")
            if instance_id not in metrics_map:
                metrics_map[instance_id] = []
            metrics_map[instance_id].append(metric_info["value"][1])

        result = {instance_id: method(values) for instance_id, values in metrics_map.items()}
        return result

    def compare_event(self, aggregation_result):
        """比较事件"""
        compare_result = []

        # 计算无数据事件
        for instance_id in self.instances:
            if instance_id not in aggregation_result:
                compare_result.append({
                    "instance_id": instance_id,
                    "value": 0,
                    "level": "no_data",
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
                    }
                    break

            # 未触发阈值的事件
            if not event:
                event = {
                    "instance_id": instance_id,
                    "value": value,
                    "level": "info",
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

        event_objs_map = {event.monitor_instance_id: event for event in event_objs}
        recovery_alerts = []
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
        MonitorAlert.objects.bulk_update(recovery_alerts, ["status", "end_event_id", "end_event_time"], batch_size=200)

    def create_alert(self, event_objs):
        """告警生成处理"""
        no_data_events, alert_events = [], []
        for event_obj in event_objs:
            if event_obj.level == "info":
                continue
            if event_obj.level == "no_data":
                no_data_events.append(event_obj)
            else:
                alert_events.append(event_obj)

        # 正常告警
        alert_objs = [
            MonitorAlert(
                policy_id=self.policy.id,
                monitor_instance_id=event_obj.monitor_instance_id,
                alert_type="alert",
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
        metrics = self.query_metrics()
        aggregation_result = self.metric_aggregation(metrics)
        events = self.compare_event(aggregation_result)
        event_objs = self.create_event(events)
        self.alert_handling(event_objs)
