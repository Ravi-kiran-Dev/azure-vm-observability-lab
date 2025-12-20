# Key Learnings

This document captures the key technical and architectural learnings from building the
**Azure VM Observability Lab**.  
Each section corresponds to a project phase and reflects real-world Azure monitoring behavior.

---

## Step 1 – Monitoring Foundation (Terraform + Log Analytics)

- Observability should start with a centralized log sink before deploying compute resources.
- Log Analytics Workspace design impacts cost, retention, and query performance.
- Consistent tagging across resources simplifies governance and cost tracking.
- Pinning Terraform provider versions avoids unexpected breaking changes.
- Infrastructure-as-Code repositories must exclude build artifacts and local state files.

---

## Step 2 – VM Provisioning and Telemetry Enablement

- Azure VM SKU availability can vary by region and time due to capacity constraints.
- VM diagnostic settings are resource-specific and do not support all log categories.
- Azure Virtual Machines primarily support **metrics** at the resource level.
- Control-plane logs (Administrative, Policy, ServiceHealth) are emitted at the **subscription scope** via AzureActivity.
- Guest OS logs require Azure Monitor Agent (AMA) and are separate from platform diagnostics.
- Azure Monitor telemetry pipelines are asynchronous; ingestion delays are expected.

---

## Step 3 – KQL-Based Observability

- AzureActivity provides control-plane visibility for resource lifecycle and management operations.
- AzureMetrics is ideal for performance monitoring and alert-driven use cases.
- Metrics and logs serve different purposes: metrics for fast detection, logs for deep investigation.
- Time binning in KQL helps reduce alert noise and highlights sustained trends.
- Writing KQL with alerting and RCA in mind leads to more actionable monitoring.
- Validation of telemetry using KQL is essential before building alerts or dashboards.

---

## Overall Takeaways

- Azure monitoring requires combining multiple telemetry sources: metrics, platform logs, and guest logs.
- Diagnostic settings must be tailored to each Azure resource type.
- Proper observability design balances visibility, cost, and signal-to-noise ratio.
- Documenting issues, resolutions, and learnings strengthens operational maturity.
