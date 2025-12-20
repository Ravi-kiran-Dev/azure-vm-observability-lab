# vm_metrics_report.py
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
from auth import get_credential

WORKSPACE_ID = "d49f9fc5-36a6-4a1e-af72-b3ace4bb414c"


def get_vm_cpu_metrics():
    client = LogsQueryClient(get_credential())

    query = """
    AzureMetrics
    | where MetricName == "Percentage CPU"
    | summarize AvgCPU = avg(Average) by bin(TimeGenerated, 5m)
    | sort by TimeGenerated desc
    """

    response = client.query_workspace(
        WORKSPACE_ID,
        query,
        timespan=timedelta(hours=1)
    )

    if response.tables:
        return response.tables[0].rows
    return []


if __name__ == "__main__":
    data = get_vm_cpu_metrics()
    print("VM CPU Metrics (Last 1h)")
    print(data[:5])
