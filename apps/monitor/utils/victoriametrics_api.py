import requests

from apps.monitor.constants import VICTORIAMETRICS_HOST, VICTORIAMETRICS_USER, VICTORIAMETRICS_PWD


class VictoriaMetricsAPI:
    def __init__(self):
        self.host = VICTORIAMETRICS_HOST
        self.username = VICTORIAMETRICS_USER
        self.password = VICTORIAMETRICS_PWD

    def query(self, query):
        response = requests.get(
            f"{self.host}/api/v1/query",
            params={"query": query},
            auth=(self.username, self.password),
        )
        response.raise_for_status()
        return response.json()

    def query_range(self, query, start, end, step):
        response = requests.get(
            f"{self.host}/api/v1/query_range",
            params={"query": query, "start": start, "end": end, "step": step},
            auth=(self.username, self.password),
        )
        response.raise_for_status()
        return response.json()
