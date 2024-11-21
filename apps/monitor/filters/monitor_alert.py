from django_filters import FilterSet, CharFilter, DateFromToRangeFilter

from apps.monitor.models.monitor_policy import MonitorAlert


class MonitorAlertFilter(FilterSet):
    status = CharFilter(field_name="status", lookup_expr="exact", label="状态")
    created_at = DateFromToRangeFilter(field_name="created_at", label="创建时间范围")

    class Meta:
        model = MonitorAlert
        fields = ["status", "created_at"]
