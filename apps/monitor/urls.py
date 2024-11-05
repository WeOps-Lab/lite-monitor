from rest_framework import routers

from apps.monitor.views.monitor_metrics import  MetricGroupVieSet, MetricVieSet
from apps.monitor.views.metrics_instance import MetricsInstanceVieSet
from apps.monitor.views.monotor_object import MonitorObjectVieSet, MonitorInstanceGroupingRuleVieSet

router = routers.DefaultRouter()
router.register(r"api/monitor_object", MonitorObjectVieSet, basename="MonitorObject")
router.register(r"api/metrics_group", MetricGroupVieSet, basename="MetricsInstance")
router.register(r"api/metrics", MetricVieSet, basename="MetricsInstance")
router.register(r"api/metrics_instance", MetricsInstanceVieSet, basename="MetricsInstance")
router.register(r"api/monitor_instance_group_rule", MonitorInstanceGroupingRuleVieSet, basename="MonitorInstanceGroupingRule")

urlpatterns = router.urls
