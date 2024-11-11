from apps.core.utils.keycloak_client import KeyCloakClient
from apps.monitor.constants import MONITOR_OBJS
from apps.monitor.models.monitor_metrics import MetricGroup, Metric
from apps.monitor.models.monitor_object import MonitorInstance, MonitorObject
from apps.core.utils.user_group import Group
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


class MonitorObjectService:
    @staticmethod
    def get_monitor_instance(monitor_object_id, token):
        """获取监控对象实例"""
        keycloak_client = KeyCloakClient()
        roles = keycloak_client.get_roles(token)
        if "admin" in roles:
            # todo default_metric_map 后续需要从数据库中获取
            default_metric_map = {i["name"]: i["default_metric"] for i in MONITOR_OBJS}
            obj = MonitorObject.objects.filter(id=monitor_object_id).first()
            metrics = VictoriaMetricsAPI().query(default_metric_map[obj.name])
            instance_set = {
                metric_info["metric"]["instance_id"]
                for metric_info in metrics.get("result", []) if metric_info.get("metric", {}).get("instance_id")
            }
            return list(instance_set)
        user_group_and_subgroup_ids = Group(token).get_user_group_and_subgroup_ids()
        objs = MonitorInstance.objects.filter(monitor_object_id=monitor_object_id, organization__in=user_group_and_subgroup_ids)
        return [i.instance_id for i in objs]

    @staticmethod
    def import_monitor_object(data: dict):
        """Import monitor object"""
        metrics = data.pop("metrics")
        monitor_obj, _ = MonitorObject.objects.update_or_create(name=data["name"], defaults=data)

        old_groups = MetricGroup.objects.filter(monitor_object=monitor_obj)
        old_groups_name = {i.name for i in old_groups}

        new_groups_name = {i["metric_group"] for i in metrics if i["metric_group"] not in old_groups_name}
        create_metric_group = [
            MetricGroup(
                monitor_object=monitor_obj,
                name=name,
            ) for name in new_groups_name
        ]
        newer_groups = MetricGroup.objects.bulk_create(create_metric_group, batch_size=200)

        groups_map = {i.name: i.id for i in old_groups}
        groups_map.update({i.name: i.id for i in newer_groups})

        metrics_to_update = []
        metrics_to_create = []
        existing_metrics = {metric.name: metric for metric in Metric.objects.filter(monitor_object=monitor_obj)}

        for metric in metrics:
            if metric["name"] in existing_metrics:
                existing_metric = existing_metrics[metric["name"]]
                existing_metric.metric_group_id = groups_map[metric["metric_group"]]
                existing_metric.display_name = metric["display_name"]
                existing_metric.type = metric["type"]
                existing_metric.query = metric["query"]
                existing_metric.unit = metric["unit"]
                existing_metric.data_type = metric["data_type"]
                existing_metric.description = metric["description"]
                existing_metric.dimensions = metric["dimensions"]
                metrics_to_update.append(existing_metric)
            else:
                metrics_to_create.append(
                    Metric(
                        monitor_object=monitor_obj,
                        metric_group_id=groups_map[metric["metric_group"]],
                        name=metric["name"],
                        display_name=metric["display_name"],
                        type=metric["type"],
                        query=metric["query"],
                        unit=metric["unit"],
                        data_type=metric["data_type"],
                        description=metric["description"],
                        dimensions=metric["dimensions"],
                    )
                )

        if metrics_to_update:
            Metric.objects.bulk_update(metrics_to_update, [
                "metric_group_id", "display_name", "type", "query", "unit", "data_type", "description", "dimensions"
            ], batch_size=200)

        if metrics_to_create:
            Metric.objects.bulk_create(metrics_to_create, batch_size=200)

    @staticmethod
    def export_monitor_object(id: int):
        """导出监控对象"""
        monitor_obj = MonitorObject.objects.prefetch_related("metric_set").get(id=id)
        metrics = monitor_obj.metric_set.all()
        data = {
            "name": monitor_obj.name,
            "type": monitor_obj.type,
            "description": monitor_obj.description,
            "metrics": [
                {
                    "metric_group": i.metric_group.name,
                    "name": i.name,
                    "display_name": i.display_name,
                    "type": i.type,
                    "query": i.query,
                    "unit": i.unit,
                    "data_type": i.data_type,
                    "description": i.description,
                    "dimensions": i.dimensions,
                } for i in metrics
            ]
        }
        return data
