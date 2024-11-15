from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.web_utils import WebUtils
from apps.monitor.filters.monitor_object import MonitorObjectFilter, MonitorInstanceGroupingRuleFilter
from apps.monitor.models.monitor_object import MonitorObject, MonitorInstanceGroupingRule
from apps.monitor.serializers.monitor_object import MonitorObjectSerializer, MonitorInstanceGroupingRuleSerializer
from apps.monitor.services.monitor_object import MonitorObjectService
from config.default import AUTH_TOKEN_HEADER_NAME
from config.drf.pagination import CustomPageNumberPagination


class MonitorObjectVieSet(viewsets.ModelViewSet):
    queryset = MonitorObject.objects.all()
    serializer_class = MonitorObjectSerializer
    filterset_class = MonitorObjectFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="monitor_object_list",
        operation_description="监控对象列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_create",
        operation_description="创建监控对象",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_update",
        operation_description="更新监控对象",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_partial_update",
        operation_description="部分更新监控对象",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_retrieve",
        operation_description="查询监控对象",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_del",
        operation_description="删除监控对象",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_import",
        operation_description="导入监控对象",
    )
    @action(methods=['post'], detail=False, url_path='import')
    def import_monitor_object(self, request):
        MonitorObjectService.import_monitor_object(request.data)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="monitor_object_export",
        operation_description="导出监控对象",
    )
    @action(methods=['get'], detail=False, url_path='export/(?P<pk>[^/.]+)')
    def export_monitor_object(self, request, pk):
        data = MonitorObjectService.export_monitor_object(pk)
        return WebUtils.response_success(data)


class MonitorInstanceGroupingRuleVieSet(viewsets.ModelViewSet):
    queryset = MonitorInstanceGroupingRule.objects.all()
    serializer_class = MonitorInstanceGroupingRuleSerializer
    filterset_class = MonitorInstanceGroupingRuleFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_list",
        operation_description="监控实例分组规则列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_create",
        operation_description="创建监控实例分组规则",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_update",
        operation_description="更新监控实例分组规则",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_partial_update",
        operation_description="部分更新监控实例分组规则",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_retrieve",
        operation_description="查询监控实例分组规则",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_instance_grouping_rule_del",
        operation_description="删除监控实例分组规则",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class MonitorInstanceVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_id="monitor_instance_list",
        operation_description="监控实例列表",
        manual_parameters=[openapi.Parameter("monitor_object_id", openapi.IN_PATH, description="指标查询参数", type=openapi.TYPE_INTEGER, required=True)],
    )
    @action(methods=['get'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/list')
    def monitor_instance_list(self, request, monitor_object_id):
        inst_list = MonitorObjectService.get_monitor_instance(
            int(monitor_object_id),
            request.META.get(AUTH_TOKEN_HEADER_NAME).split("Bearer ")[-1],
        )
        return WebUtils.response_success(inst_list)

    @swagger_auto_schema(
        operation_id="generate_monitor_instance_id",
        operation_description="生成监控实例ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "monitor_instance_name": openapi.Schema(type=openapi.TYPE_STRING, description="监控实例名称"),
                "interval": openapi.Schema(type=openapi.TYPE_INTEGER, description="监控实例采集间隔(s)"),
            },
            required=["monitor_instance_name", "interval"]
        )

    )
    @action(methods=['post'], detail=False, url_path='(?P<monitor_object_id>[^/.]+)/generate_instance_id')
    def generate_monitor_instance_id(self, request, monitor_object_id):
        result = MonitorObjectService.generate_monitor_instance_id(
            int(monitor_object_id),
            request.data["monitor_instance_name"],
            request.data["interval"],
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="autodiscover_monitor_instance",
        operation_description="自动发现监控实例",
    )
    @action(methods=['get'], detail=False, url_path='autodiscover_monitor_instance')
    def autodiscover_monitor_instance(self, request):
        MonitorObjectService.autodiscover_monitor_instance()
        return WebUtils.response_success()
