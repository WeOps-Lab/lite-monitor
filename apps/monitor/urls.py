from rest_framework import routers

from apps.monitor.views.metrics import MetricObjectVieSet, MetricGroupVieSet, MetricVieSet
from apps.monitor.views.metrics_instance import MetricsInstanceVieSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"api/metrics_object", MetricObjectVieSet, basename="MetricsInstance")
router.register(r"api/metrics_group", MetricGroupVieSet, basename="MetricsInstance")
router.register(r"api/metrics", MetricVieSet, basename="MetricsInstance")
router.register(r"api/metrics_instance", MetricsInstanceVieSet, basename="MetricsInstance")

urlpatterns = router.urls
