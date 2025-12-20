# Issues and Fixes

This document captures real issues encountered during the implementation of the
**Azure VM Observability Lab**, along with root cause analysis, resolutions, and
key learnings. These issues reflect real-world Azure and Terraform behavior.

---

## Issue 1: GitHub push failed due to large Terraform provider binaries

### Symptoms
- `git push` failed with GitHub error indicating a file exceeded 100 MB.
- Error referenced Terraform provider binary inside `.terraform/`.

### Impact
- Unable to push Terraform code to the remote repository.
- Repository was not CI/CD ready.

### Root Cause
- Terraform provider binaries inside `.terraform/` were accidentally committed.
- `.gitignore` was added after the initial commit, so files remained in Git history.

### Resolution
- Added `.terraform/`, Terraform state, and plan files to `.gitignore`.
- Removed cached binaries using:
```git rm -r --cached terraform/.terraform
- Rewrote Git history using `git filter-branch`.
- Force-pushed cleaned history to GitHub.

### Learning and Prevention
- Terraform working directories must never be committed.
- `.gitignore` should be configured before the first commit.
- Understanding Git history is critical for infrastructure repositories.

---

## Issue 2: VM deployment failed due to SKU capacity restriction

### Symptoms
- Terraform apply failed with `SkuNotAvailable` (HTTP 409).
- VM size `Standard_B2s` was unavailable in the selected region.

### Impact
- Virtual Machine could not be provisioned.
- Monitoring setup was blocked.

### Root Cause
- Azure enforces regional capacity limits on VM SKUs.
- SKU availability can change dynamically.

### Resolution
- Switched VM size to `Standard_DS1_v2`.
- Re-applied Terraform successfully without changing region.

### Learning and Prevention
- VM SKU availability varies by region and time.
- Terraform configurations should allow flexibility in VM sizing.

---

## Issue 3: Diagnostic setting failed due to unsupported Security category

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest.
- Error indicated `Security` category was not supported.

### Impact
- Diagnostic settings could not be applied to the VM.

### Root Cause
- Azure diagnostic categories are resource-specific.
- `Security` logs are not supported for VM diagnostic settings.

### Resolution
- Removed `Security` category from VM diagnostic configuration.
- Retained supported categories.

### Learning and Prevention
- Diagnostic categories must be validated per resource type.
- VM security telemetry is provided via Defender for Cloud and Sentinel.

---

## Issue 4: VM diagnostic settings failed due to unsupported Administrative category

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest.
- Azure rejected `Administrative` diagnostic category for VM.

### Impact
- VM diagnostic configuration failed again.

### Root Cause
- Azure Virtual Machines do not support platform log categories at resource level.
- Control-plane logs are emitted at subscription scope via AzureActivity.

### Resolution
- Updated VM diagnostic settings to enable **metrics only**.
- Relied on AzureActivity for control-plane visibility.

### Learning and Prevention
- VM diagnostic settings primarily support metrics.
- Logs and metrics have different scopes in Azure Monitor.

---

## Issue 5: VM and Log Analytics appeared disconnected

### Symptoms
- VM and Log Analytics Workspace were created successfully.
- No control-plane logs appeared in Log Analytics initially.

### Impact
- Monitoring appeared incomplete.
- Required clarification of telemetry paths.

### Root Cause
- AzureActivity logs originate at the **subscription level**.
- Subscription-level diagnostic settings were missing initially.

### Resolution
- Added subscription-level diagnostic settings.
- Routed AzureActivity logs to Log Analytics Workspace.

### Learning and Prevention
- Azure Monitor uses multiple telemetry pipelines.
- Subscription-level diagnostics are required for control-plane visibility.

---

## Issue 6: AzureActivity logs not visible immediately after configuration

### Symptoms
- AzureMetrics data was visible.
- AzureActivity table remained empty initially.

### Impact
- Temporary uncertainty about monitoring correctness.

### Root Cause
- Azure Monitor ingests AzureActivity logs asynchronously.
- Ingestion delay is expected behavior.

### Resolution
- Waited for ingestion pipeline to stabilize.
- AzureActivity logs appeared without configuration changes.

### Learning and Prevention
- AzureActivity ingestion is not instantaneous.
- Validation should include time-based rechecks before assuming failure.

---

## Issue 7: Terraform alert creation failed due to missing action block

### Symptoms
- Terraform plan failed with error:
`Insufficient action blocks`.
- Alert resources could not be created.

### Impact
- KQL-based alerts were blocked from deployment.

### Root Cause
- `azurerm_monitor_scheduled_query_rules_alert` requires at least one `action` block.
- Action Group was not defined initially.

### Resolution
- Created an Azure Monitor Action Group.
- Added `action` block referencing the Action Group to all alerts.
- Terraform plan and apply succeeded.

### Learning and Prevention
- Azure Monitor alerts always require an action target.
- Even test alerts must include an action group.
- Terraform validation errors often reflect Azure API requirements.
