from django_filters import CharFilter, FilterSet

from apps.monitor.models.monitor_metrics import MetricGroup, Metric


class MetricGroupFilter(FilterSet):
    monitor_object = CharFilter(field_name="monitor_object__name", lookup_expr="exact", label="指标对象名称")

    class Meta:
        model = MetricGroup
        fields = ["monitor_object"]


class MetricFilter(FilterSet):
    monitor_object = CharFilter(field_name="monitor_object__name", lookup_expr="exact", label="指标对象名称")

    class Meta:
        model = Metric
        fields = ["monitor_object"]
