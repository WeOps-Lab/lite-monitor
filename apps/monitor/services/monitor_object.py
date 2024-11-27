import uuid

from django.db.models import Prefetch

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.monitor.constants import MONITOR_OBJS
from apps.monitor.models.monitor_metrics import MetricGroup, Metric
from apps.monitor.models.monitor_object import MonitorInstance, MonitorObject
from apps.core.utils.user_group import Group
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI
from apps.monitor.tasks.grouping_rule import sync_instance_and_group

class MonitorObjectService:

    @staticmethod
    def get_instances_by_metric(metric: str):
        """获取监控对象实例"""
        metrics = VictoriaMetricsAPI().query(metric)
        instance_map = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = metric_info.get("metric", {}).get("instance_id")
            if not instance_id:
                continue
            agent_id = metric_info.get("metric", {}).get("agent_id")
            _time = metric_info["value"][0]

            if instance_id not in instance_map:
                instance_map[instance_id] = {"instance_id": instance_id, "agent_id": agent_id, "time": _time}
            else:
                if _time > instance_map[instance_id]["time"]:
                    instance_map[instance_id] = {"instance_id": instance_id, "agent_id": agent_id, "time": _time}

        return instance_map

    @staticmethod
    def get_object_instances(monitor_object_id):
        # todo default_metric_map 后续需要从数据库中获取
        default_metric_map = {i["name"]: i["default_metric"] for i in MONITOR_OBJS}
        monitor_obj = MonitorObject.objects.filter(id=monitor_object_id).first()
        return MonitorObjectService.get_instances_by_metric(default_metric_map[monitor_obj.name])

    @staticmethod
    def get_monitor_instance(monitor_object_id, token):
        """获取监控对象实例"""
        keycloak_client = KeyCloakClient()
        roles = keycloak_client.get_roles(token)
        instance_map = MonitorObjectService.get_object_instances(monitor_object_id)
        result = []

        if "admin" in roles:
            objs = MonitorInstance.objects.filter(monitor_object_id=monitor_object_id,).prefetch_related(
                Prefetch('monitorinstanceorganization_set', to_attr='organizations'))
        else:
            user_group_and_subgroup_ids = Group(token).get_user_group_and_subgroup_ids()
            objs = MonitorInstance.objects.filter(
                monitor_object_id=monitor_object_id,
                monitorinstanceorganization__organization__in=user_group_and_subgroup_ids
            ).prefetch_related(
                Prefetch('monitorinstanceorganization_set', to_attr='organizations')
            )

        for obj in objs:
            result.append({
                "instance_id": obj.id,
                "instance_name": obj.name,
                "agent_id": instance_map.get(obj.id, {}).get("agent_id", ""),
                "organization": [i.organization for i in obj.organizations],
                "time": instance_map.get(obj.id, {}).get("time", ""),
            })

        return result

    @staticmethod
    def generate_monitor_instance_id(monitor_object_id, monitor_instance_name, interval):
        """生成监控对象实例ID"""
        obj = MonitorInstance.objects.filter(monitor_object_id=monitor_object_id, name=monitor_instance_name).first()
        if obj:
            obj.interval = interval
            obj.save()
            return obj.id
        else:
            # 生成一个uui
            instance_id = uuid.uuid4().hex
            MonitorInstance.objects.create(
                id=instance_id, name=monitor_instance_name, interval=interval, monitor_object_id=monitor_object_id)

            return instance_id

    @staticmethod
    def import_monitor_object(data: dict):
        """Import monitor object"""
        if data.get("is_compound_object"):
            MonitorObjectService.import_compound_monitor_object(data)
        else:
            MonitorObjectService.import_basic_monitor_object(data)

    @staticmethod
    def import_basic_monitor_object(data: dict):
        """导入基础监控对象"""
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

        return monitor_obj

    @staticmethod
    def import_compound_monitor_object(data: dict):
        """导入复合监控对象"""
        base_object = {}
        derivative_objects = []
        for object_info in data.get("objects", []):
            if object_info.get("level") == "base":
                base_object = object_info
            else:
                derivative_objects.append(object_info)

        base_obj = MonitorObjectService.import_basic_monitor_object(base_object)
        for derivative_object in derivative_objects:
            derivative_object["parent"] = base_obj
            MonitorObjectService.import_basic_monitor_object(derivative_object)

    @staticmethod
    def export_monitor_object(id: int):
        """导出监控对象"""
        monitor_obj = MonitorObject.objects.prefetch_related("metric_set").get(id=id)
        if monitor_obj.level != "base" or monitor_obj.parent:
            raise ValueError("Only base monitor object can be exported")
        children = monitor_obj.children.all()
        if children:
            return MonitorObjectService.export_compound_monitor_object(monitor_obj, children)
        else:
            return MonitorObjectService.export_basic_monitor_object(monitor_obj)

    @staticmethod
    def export_basic_monitor_object(monitor_obj):
        """导出基础监控对象"""
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

    @staticmethod
    def export_compound_monitor_object(monitor_obj, children):
        """导出复合监控对象"""
        data = {"is_compound_object": True, "objects": [MonitorObjectService.export_basic_monitor_object(monitor_obj)]}
        for child in children:
            data["objects"].append(MonitorObjectService.export_basic_monitor_object(child.id))
        return data

    @staticmethod
    def autodiscover_monitor_instance():
        """同步监控实例数据"""
        sync_instance_and_group.delay()
