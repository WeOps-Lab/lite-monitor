from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.web_utils import WebUtils
from apps.monitor.services.metrics import Metrics


class MetricsVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_id="metrics",
        operation_description="查询指标信息",
        manual_parameters=[
            openapi.Parameter("query", openapi.IN_QUERY, description="指标查询参数", type=openapi.TYPE_STRING),
        ],
        required=["query"]
    )
    @action(methods=['get'], detail=False, url_path='metrics')
    def get_metrics(self, request):
        data = Metrics.get_metrics(request.GET.get('query'))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="metrics",
        operation_description="查询指标信息",
        manual_parameters=[
            openapi.Parameter("query", openapi.IN_QUERY, description="指标查询参数", type=openapi.TYPE_STRING),
            openapi.Parameter("start", openapi.IN_QUERY, description="开始时间", type=openapi.TYPE_STRING),
            openapi.Parameter("end", openapi.IN_QUERY, description="结束时间", type=openapi.TYPE_STRING),
            openapi.Parameter("step", openapi.IN_QUERY, description="指标采集间隔", type=openapi.TYPE_STRING),
        ],
        required=["query"]
    )
    @action(methods=['get'], detail=False, url_path='metrics_range')
    def get_metrics_range(self, request):
        data = Metrics.get_metrics_range(
            request.GET.get('query'),
            request.GET.get('start'),
            request.GET.get('end'),
            request.GET.get('step'),
        )
        return WebUtils.response_success(data)
