from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.web_utils import WebUtils
from apps.monitor.models import MonitorAlert, MonitorEvent
from apps.monitor.filters.monitor_alert import MonitorAlertFilter
from apps.monitor.serializers.monitor_alert import MonitorAlertSerializer
from config.drf.pagination import CustomPageNumberPagination


class MonitorAlertVieSet(viewsets.ModelViewSet):
    queryset = MonitorAlert.objects.all().order_by("-created_at")
    serializer_class = MonitorAlertSerializer
    filterset_class = MonitorAlertFilter
    pagination_class = CustomPageNumberPagination


class MonitorEventVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="查询告警事件",
        manual_parameters=[
            openapi.Parameter("alert_id", openapi.IN_PATH, description="告警id", type=openapi.TYPE_INTEGER, required=True),
        ],
    )
    @action(methods=['get'], detail=False, url_path='query/(?P<alert_id>[^/.]+)')
    def get_events(self, request, alert_id):
        alert_obj = MonitorAlert.objects.get(id=alert_id)
        events = MonitorEvent.objects.filter(
            policy_id=alert_obj.policy_id,
            monitor_instance_id=alert_obj.monitor_instance_id,
            created_at__gte=alert_obj.start_event_time,
            created_at__lte=alert_obj.end_event_time,
        ).order_by("-created_at")
        result = [
            {
                "id": i.id,
                "level": i.level,
                "value": i.value,
                "created_at": i.created_at,
                "monitor_instance_id": i.monitor_instance_id,
                "policy_id": i.policy_id,
            }
            for i in events
        ]
        return WebUtils.response_success(result)
