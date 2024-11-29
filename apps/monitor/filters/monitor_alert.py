from django_filters import FilterSet, CharFilter, IsoDateTimeFromToRangeFilter

from apps.monitor.models.monitor_policy import MonitorAlert


class MonitorAlertFilter(FilterSet):
    status_in = CharFilter(field_name="status", lookup_expr="in", label="状态")
    level_in = CharFilter(field_name="level", lookup_expr="in", label="告警级别")
    created_at = IsoDateTimeFromToRangeFilter(field_name="created_at", label="创建时间范围")

    class Meta:
        model = MonitorAlert
        fields = ["status_in", "level_in", "created_at"]
