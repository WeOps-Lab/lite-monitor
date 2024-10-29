from rest_framework import serializers

from apps.monitor.models.metrics import MetricObject, MetricGroup, Metric


class MetricObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricObject
        fields = '__all__'


class MetricGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricGroup
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
