resource "azurerm_monitor_action_group" "default_ag" {
  name                = "ag-vm-observability"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "vmobs"

  email_receiver {
    name          = "primary-email"
    email_address = "example@example.com"
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert" "failed_operations" {
  name                = "alert-failed-azure-operations"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  data_source_id = azurerm_log_analytics_workspace.law.id
  description    = "Alert on failed Azure control-plane operations"
  enabled        = true
  severity       = 2

  query = <<-KQL
    AzureActivity
    | where ActivityStatusValue == "Failed"
  KQL

  frequency   = 5
  time_window = 15

  trigger {
    operator  = "GreaterThan"
    threshold = 0
  }

   action {
    action_group = [
      azurerm_monitor_action_group.default_ag.id
    ]
  }
}


resource "azurerm_monitor_scheduled_query_rules_alert" "high_cpu_vm" {
  name                = "alert-vm-high-cpu"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  data_source_id = azurerm_log_analytics_workspace.law.id
  description    = "Alert on sustained high CPU usage for VM"
  enabled        = true
  severity       = 3

  query = <<-KQL
    AzureMetrics
    | where MetricName == "Percentage CPU"
    | summarize AvgCPU = avg(Average) by bin(TimeGenerated, 5m)
    | where AvgCPU > 80
  KQL

  frequency   = 5
  time_window = 15

  trigger {
    operator  = "GreaterThan"
    threshold = 0
  }

  action {
    action_group = [
      azurerm_monitor_action_group.default_ag.id
    ]
  }
}
