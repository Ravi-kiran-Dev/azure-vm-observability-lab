# Issues and Fixes

This document records real-world issues encountered during the implementation of the
Azure VM Observability Lab, along with root cause analysis, resolutions, and learnings.
The intent is to demonstrate practical troubleshooting and operational thinking.

---

## Issue 1: GitHub push failed due to large Terraform provider binaries

### Symptoms
- `git push` failed with GitHub error indicating file size exceeded 100 MB
- Error referenced Terraform provider binary inside `.terraform/`

### Impact
- Repository could not be pushed to GitHub
- Project collaboration and CI/CD readiness blocked

### Root Cause
- Terraform provider binaries inside `.terraform/` were accidentally committed
- `.gitignore` was added after files were already tracked
- Git continued tracking the files in commit history

### Resolution
- Added `.terraform/` and Terraform state files to `.gitignore`
- Removed cached binaries using `git rm --cached`
- Rewrote Git history using `git filter-branch`
- Force-pushed cleaned repository

### Learning and Prevention
- Terraform working directories must never be committed
- `.gitignore` must be configured before first commit
- Understanding Git history is critical for IaC repositories

---

## Issue 2: VM deployment failed due to SKU capacity restriction

### Symptoms
- Terraform apply failed with `SkuNotAvailable` (HTTP 409)
- Error indicated `Standard_B2s` unavailable in `eastus`

### Impact
- VM provisioning blocked
- Monitoring pipeline could not proceed

### Root Cause
- Azure enforces regional capacity constraints on VM SKUs
- Requested SKU temporarily unavailable

### Resolution
- Switched VM size to `Standard_DS1_v2`
- Re-applied Terraform successfully without changing region

### Learning and Prevention
- VM SKU availability varies by region and time
- Terraform configs should allow flexibility in VM sizing
- SKU validation is important for production deployments

---

## Issue 3: VM diagnostic setting failed due to unsupported Security category

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest
- Error: `Category 'Security' is not supported`

### Impact
- Diagnostic settings could not be applied to VM
- Log ingestion incomplete

### Root Cause
- Azure VM diagnostic settings do not support `Security` logs
- Security telemetry is provided via Defender for Cloud and Sentinel

### Resolution
- Removed unsupported `Security` category from VM diagnostics
- Retained supported telemetry paths

### Learning and Prevention
- Diagnostic categories are resource-specific
- Security logs must be sourced from appropriate Azure services

---

## Issue 4: VM diagnostic setting failed due to unsupported Administrative category

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest
- Error: `Category 'Administrative' is not supported`

### Impact
- VM diagnostics could not be enabled as expected

### Root Cause
- Azure Virtual Machines do not emit platform logs at resource level
- Administrative logs originate at subscription scope via AzureActivity

### Resolution
- Updated VM diagnostic settings to enable only supported metrics
- Relied on AzureActivity for control-plane visibility

### Learning and Prevention
- VM diagnostics ≠ control-plane logs
- Monitoring must account for telemetry scope and source

---

## Issue 5: VM and Log Analytics appeared disconnected

### Symptoms
- VM and Log Analytics Workspace created successfully
- No control-plane logs visible in Log Analytics initially

### Impact
- Monitoring appeared incomplete
- Required clarification of telemetry flow

### Root Cause
- VM diagnostic settings send metrics only
- Subscription-level diagnostic settings were missing

### Resolution
- Added subscription-level diagnostic settings
- Routed AzureActivity logs to Log Analytics

### Learning and Prevention
- Azure Monitor uses multiple telemetry pipelines
- Subscription diagnostics are required for AzureActivity logs

---

## Issue 6: AzureActivity logs not visible immediately

### Symptoms
- AzureMetrics data visible
- AzureActivity table initially empty

### Impact
- Perceived misconfiguration
- Required validation before proceeding

### Root Cause
- AzureActivity ingestion is asynchronous
- Log flow is delayed even with correct configuration

### Resolution
- Waited for ingestion delay (5–15 minutes)
- Revalidated logs without changing configuration

### Learning and Prevention
- Azure Monitor ingestion delays are normal
- Patience and validation are part of production operations

---

## Issue 7: Terraform alert creation failed due to missing action blocks

### Symptoms
- Terraform plan failed with error:
  `At least 1 "action" blocks are required`

### Impact
- KQL-based alert rules could not be created

### Root Cause
- Azure Monitor Scheduled Query Rules require at least one action group
- Alerts cannot exist without an action target

### Resolution
- Created an Azure Monitor Action Group
- Linked alerts to the action group using `action` blocks

### Learning and Prevention
- Azure alerts are incomplete without actions
- Action Groups are mandatory even for test alerts

### Observation: Python automation returned empty results

- Python script executed successfully and queried Log Analytics.
- Query returned an empty DataFrame for failed operations.

**Explanation:**
- No failed Azure control-plane operations occurred within the selected time window.

**Learning:**
- Empty query results can indicate healthy systems.
- Automation scripts should handle and report empty datasets gracefully.

