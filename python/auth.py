# auth.py
from azure.identity import DefaultAzureCredential


def get_credential():
    """
    Uses DefaultAzureCredential to authenticate with Azure.
    Works with az login, managed identity, or service principal.
    """
    return DefaultAzureCredential()
