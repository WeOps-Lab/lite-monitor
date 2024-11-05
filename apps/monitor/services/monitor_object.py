from joblib.externals.cloudpickle import instance

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.monitor.constants import MONITOR_OBJS
from apps.monitor.models.monitor_object import MonitorInstance, MonitorObject
from apps.monitor.utils.user_group import Group
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


class MonitorObjectService:
    @staticmethod
    def get_monitor_instance(monitor_object_id, token):
        """获取监控对象实例"""
        keycloak_client = KeyCloakClient()
        roles = keycloak_client.get_roles(token)
        if "admin" in roles:
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
