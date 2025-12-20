# Key Learnings

This document captures the technical and architectural learnings from building the
Azure VM Observability Lab. Each section reflects real-world Azure monitoring behavior
and operational decision-making.

---

## Step 1 – Monitoring Foundation (Terraform + Log Analytics)

- Observability should start with a centralized log sink before deploying compute resources.
- Log Analytics Workspace design impacts cost, retention, and query performance.
- Consistent tagging enables governance, cost tracking, and operational clarity.
- Terraform provider versions should be pinned to avoid breaking changes.
- Infrastructure repositories must exclude build artifacts and local state files using `.gitignore`.

---

## Step 2 – VM Provisioning and Telemetry Enablement

- Azure VM SKU availability can vary by region due to capacity constraints.
- VM diagnostic settings are resource-specific and do not support all log categories.
- Azure Virtual Machines primarily support **metrics** at the resource level.
- Control-plane logs (Administrative, Policy, ServiceHealth) are emitted at the **subscription scope** via AzureActivity.
- Guest OS logs require Azure Monitor Agent (AMA) and are separate from platform diagnostics.
- Azure Monitor telemetry pipelines are asynchronous; ingestion delays are expected and normal.

---

## Step 3 – KQL-Based Observability

- AzureActivity provides control-plane visibility for deployments, updates, and failures.
- AzureMetrics is ideal for performance monitoring and alert-driven use cases.
- Metrics and logs serve different purposes: metrics for fast detection, logs for deep RCA.
- Time binning in KQL reduces alert noise and highlights sustained trends.
- KQL should be written with alerting and investigation use cases in mind.
- Telemetry must be validated using KQL before building alerts or automation.

---

## Step 4 – Alert Design Using KQL

- Log-based alerts provide richer context than metric-only alerts.
- Alert rules must include action groups; otherwise, Terraform validation fails.
- Alert thresholds should detect sustained conditions, not transient spikes.
- Time window and evaluation frequency tuning is critical to avoid alert fatigue.
- KQL reuse across dashboards and alerts improves consistency and maintainability.
- Alert execution may be delayed after creation due to Azure Monitor scheduling behavior.

---

## Step 5 – Automation Using Python

- Log Analytics data can be queried programmatically using Azure Monitor APIs.
- Python automation enables enrichment, reporting, and downstream workflows.
- Empty query results do not always indicate failure; they may reflect healthy systems.
- Automation scripts must handle empty datasets gracefully.
- Observability automation should support insight generation, not just data retrieval.

---

---
## Workbooks

- Workbooks are the preferred way to build Azure Monitor dashboards.
- Empty query results often indicate healthy systems, not broken queries.
- Dashboards should combine metrics, logs, and tables for context.


## Overall Takeaways

- Azure observability requires combining metrics, platform logs, and automation.
- Diagnostic scope (resource vs subscription) is critical to correct monitoring design.
- Real-world monitoring includes delays, empty datasets, and non-deterministic behavior.
- Documenting issues, fixes, and learnings reflects strong operational maturity.
