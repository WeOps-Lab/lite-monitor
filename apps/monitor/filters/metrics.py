from django_filters import CharFilter, FilterSet

from apps.monitor.models.metrics import MetricObject, MetricGroup, Metric


class MetricObjectFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="指标对象名称")
    type = CharFilter(field_name="type", lookup_expr="exact", label="指标对象类型")

    class Meta:
        model = MetricObject
        fields = ["name", "type"]


class MetricGroupFilter(FilterSet):
    metric_object = CharFilter(field_name="metric_object__name", lookup_expr="exact", label="指标对象名称")

    class Meta:
        model = MetricGroup
        fields = ["metric_object"]


class MetricFilter(FilterSet):
    metric_object = CharFilter(field_name="metric_object__name", lookup_expr="exact", label="指标对象名称")

    class Meta:
        model = Metric
        fields = ["metric_object"]