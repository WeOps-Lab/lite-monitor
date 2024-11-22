from rest_framework import viewsets

from apps.monitor.filters.monitor_policy import MonitorPolicyFilter
from apps.monitor.models.monitor_policy import MonitorPolicy
from apps.monitor.serializers.monitor_policy import MonitorPolicySerializer
from config.drf.pagination import CustomPageNumberPagination
from celery import current_app
from celery.schedules import crontab
from apps.monitor.tasks.monitor_policy import scan_policy_task

class MonitorPolicyVieSet(viewsets.ModelViewSet):
    queryset = MonitorPolicy.objects.all()
    serializer_class = MonitorPolicySerializer
    filterset_class = MonitorPolicyFilter
    pagination_class = CustomPageNumberPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        policy_id = response.data['id']
        schedule = request.data.get('schedule')
        self.update_or_create_task(policy_id, schedule)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        policy_id = kwargs['pk']
        schedule = request.data.get('schedule')
        self.update_or_create_task(policy_id, schedule)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        policy_id = kwargs['pk']
        schedule = request.data.get('schedule')
        self.update_or_create_task(policy_id, schedule)
        return response

    def update_or_create_task(self, policy_id, schedule):
        task_name = f'scan_policy_task_{policy_id}'

        # 移除旧的定时任务
        current_app.control.revoke(task_name, terminate=True)

        # 添加新的定时任务
        current_app.add_periodic_task(
            crontab(schedule),
            scan_policy_task.s(policy_id),
            name=task_name
        )