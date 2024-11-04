from rest_framework import serializers

from apps.monitor.models.monitor_metrics import MetricGroup, Metric


class MetricGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricGroup
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
