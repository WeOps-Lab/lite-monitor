from rest_framework import serializers

from apps.monitor.models import MonitorPlugin


class MonitorPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorPlugin
        fields = '__all__'
