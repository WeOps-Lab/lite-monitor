from rest_framework import viewsets

from apps.monitor.filters.monitor_policy import MonitorPolicyFilter
from apps.monitor.models.monitor_policy import MonitorPolicy
from apps.monitor.serializers.monitor_policy import MonitorPolicySerializer
from config.drf.pagination import CustomPageNumberPagination


class MonitorPolicyVieSet(viewsets.ModelViewSet):
    queryset = MonitorPolicy.objects.all()
    serializer_class = MonitorPolicySerializer
    filterset_class = MonitorPolicyFilter
    pagination_class = CustomPageNumberPagination
