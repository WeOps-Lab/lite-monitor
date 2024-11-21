from rest_framework import routers

from apps.monitor.views.monitor_alert import MonitorAlertVieSet, MonitorEventVieSet
from apps.monitor.views.monitor_metrics import  MetricGroupVieSet, MetricVieSet
from apps.monitor.views.metrics_instance import MetricsInstanceVieSet
from apps.monitor.views.monitor_object import MonitorObjectVieSet, MonitorInstanceGroupingRuleVieSet, \
    MonitorInstanceVieSet
from apps.monitor.views.monitor_policy import MonitorPolicyVieSet

router = routers.DefaultRouter()
router.register(r"api/monitor_object", MonitorObjectVieSet, basename="MonitorObject")
router.register(r"api/metrics_group", MetricGroupVieSet, basename="MetricsInstance")
router.register(r"api/metrics", MetricVieSet, basename="MetricsInstance")
router.register(r"api/metrics_instance", MetricsInstanceVieSet, basename="MetricsInstance")
router.register(r"api/monitor_instance_group_rule", MonitorInstanceGroupingRuleVieSet, basename="MonitorInstanceGroupingRule")
router.register(r"api/monitor_instance", MonitorInstanceVieSet, basename="MonitorInstanceVieSet")
router.register(r"api/monitor_policy", MonitorPolicyVieSet, basename="MonitorPolicyVieSet")

router.register(r"api/monitor_alert", MonitorAlertVieSet, basename="MonitorAlertVieSet")
router.register(r"api/monitor_event", MonitorEventVieSet, basename="MonitorEventVieSet")

urlpatterns = router.urls
