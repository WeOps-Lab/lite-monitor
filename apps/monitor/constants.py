import os

# victoriametrics服务信息
VICTORIAMETRICS_HOST = os.getenv("VICTORIAMETRICS_HOST")
VICTORIAMETRICS_USER = os.getenv("VICTORIAMETRICS_USER")
VICTORIAMETRICS_PWD = os.getenv("VICTORIAMETRICS_PWD")

# 内置的监控对象
MONITOR_OBJS = [
    {"type": "OS", "name": "Host", "default_metric": 'node_procs_running_gauge{instance_type="os"}'},
    {"type": "Web", "name": "Website", "default_metric": "probe_http_status_code_gauge"},
    {"type": "K8S", "name": "K8S", "default_metric": "internal_write_write_time_ns"},
]