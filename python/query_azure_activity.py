# query_azure_activity.py
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
from auth import get_credential

WORKSPACE_ID = "d49f9fc5-36a6-4a1e-af72-b3ace4bb414c"


def get_failed_operations():
    client = LogsQueryClient(get_credential())

    query = """
    AzureActivity
    | where TimeGenerated > ago(24h)
    | where ActivityStatusValue == "Failed"
    | project TimeGenerated, ResourceGroup, Resource, OperationNameValue, Caller
    """

    response = client.query_workspace(
        WORKSPACE_ID,
        query,
        timespan=timedelta(days=1)
    )

    if response.tables:
        return response.tables[0].rows
    return []


if __name__ == "__main__":
    results = get_failed_operations()
    print("Failed Azure Operations (Last 24h)")
    print(results if results else "No failures detected")
