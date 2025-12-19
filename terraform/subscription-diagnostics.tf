data "azurerm_subscription" "current" {}

resource "azurerm_monitor_diagnostic_setting" "subscription_diagnostics" {
  name                       = "sub-activity-to-law"
  target_resource_id         = data.azurerm_subscription.current.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_log {
    category = "Administrative"
  }

  enabled_log {
    category = "Policy"
  }

  enabled_log {
    category = "ServiceHealth"
  }

  enabled_log {
    category = "Security"
  }
}
