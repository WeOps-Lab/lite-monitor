from rest_framework import routers

from apps.monitor.views.metrics import MetricsVieSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"api/metrics", MetricsVieSet, basename="Metrics")

urlpatterns = router.urls
