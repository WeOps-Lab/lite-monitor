from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.monitor.filters.monitor_metrics import MetricGroupFilter, MetricFilter
from apps.monitor.serializers.monitor_metrics import MetricGroupSerializer, MetricSerializer
from apps.monitor.models.monitor_metrics import MetricGroup, Metric
from config.drf.pagination import CustomPageNumberPagination


class MetricGroupVieSet(viewsets.ModelViewSet):
    queryset = MetricGroup.objects.all()
    serializer_class = MetricGroupSerializer
    filterset_class = MetricGroupFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="metrics_group_list",
        operation_description="指标分组列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_create",
        operation_description="创建指标分组",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_update",
        operation_description="更新指标分组",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_partial_update",
        operation_description="部分更新指标分组",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_retrieve",
        operation_description="查询指标分组",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_group_del",
        operation_description="删除指标分组",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MetricVieSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    filterset_class = MetricFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="metrics_list",
        operation_description="指标列表",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_create",
        operation_description="创建指标",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_update",
        operation_description="更新指标",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_partial_update",
        operation_description="部分更新指标",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_retrieve",
        operation_description="查询指标",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="metrics_del",
        operation_description="删除指标",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
