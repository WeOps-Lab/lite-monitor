import os

# victoriametrics服务信息
VICTORIAMETRICS_HOST = os.getenv("VICTORIAMETRICS_HOST")
VICTORIAMETRICS_USER = os.getenv("VICTORIAMETRICS_USER")
VICTORIAMETRICS_PWD = os.getenv("VICTORIAMETRICS_PWD")

# 内置的监控对象
MONITOR_OBJS = [
    {"type": "OS", "name": "Host", "default_metric": 'node_load1_gauge{instance_type="os"}'},
    {"type": "Web", "name": "Website", "default_metric": "probe_duration_seconds_gauge"},
    {"type": "K8S", "name": "Cluster", "default_metric": 'internal_write_write_time_ns{instance_type="k8s"}'},
]

# 监控策略的计算方法
POLICY_METHODS = {
    "sum": sum,
    "avg": lambda x: sum(x) / len(x),
    "max": max,
    "min": min,
    "count": len,
}

# 阀值对比方法
THRESHOLD_METHODS = {
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
}