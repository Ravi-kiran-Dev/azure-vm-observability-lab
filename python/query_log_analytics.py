from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import timedelta
import pandas as pd

WORKSPACE_ID = "d49f9fc5-36a6-4a1e-af72-b3ace4bb414c"

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

query = """
AzureActivity
| where TimeGenerated > ago(24h)
| project TimeGenerated, ResourceGroup, Resource, OperationNameValue, Caller
"""

response = client.query_workspace(
    workspace_id=WORKSPACE_ID,
    query=query,
    timespan=timedelta(days=1)
)

if response.tables:
    df = pd.DataFrame(response.tables[0].rows,
                      columns=response.tables[0].columns)
    print("Azure Operations (Last 24h)")
    print(df)
else:
    print("No failed operations detected.")
