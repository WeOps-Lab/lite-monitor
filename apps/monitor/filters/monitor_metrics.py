from django_filters import CharFilter, FilterSet

from apps.monitor.models.monitor_metrics import MetricGroup, Metric


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
