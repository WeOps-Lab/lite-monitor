from rest_framework import serializers

from apps.monitor.models.monitor_policy import MonitorAlert
from apps.monitor.serializers.monitor_instance import MonitorInstanceSerializer
from apps.monitor.serializers.monitor_policy import MonitorPolicySerializer


class MonitorAlertSerializer(serializers.ModelSerializer):
    # 使用关联的序列化器来嵌套关联对象
    policy = MonitorPolicySerializer(read_only=True)  # 关联的 MonitorPolicy 数据
    monitor_instance = MonitorInstanceSerializer(read_only=True)  # 关联的 MonitorInstance 数据

    class Meta:
        model = MonitorAlert
        fields = '__all__'
