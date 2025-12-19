# Issues and Fixes

This document captures real issues encountered during the implementation of the Azure VM Observability Lab,
along with root cause analysis, resolution steps, and key learnings.

## Issue 1: GitHub push failed due to large Terraform provider binaries

### Symptoms
- `git push` failed with GitHub error:
  > File exceeds GitHub's 100MB file size limit
- Push was rejected even after adding `.gitignore`

### Impact
- Unable to push Terraform code to remote repository
- CI/CD readiness blocked due to repository inconsistency

### Root Cause
- Terraform provider binaries inside `.terraform/` were accidentally tracked
- `.gitignore` was added **after** the files had already been committed
- Git continued to track the files in commit history

### Resolution
- Added `.terraform/` and Terraform state files to `.gitignore`
- Removed cached provider binaries using:
  ```bash
  git rm -r --cached terraform/.terraform
- Rewrote Git history to completely remove the large binary files:
  ```bash
  git filter-branch --index-filter "git rm -r --cached --ignore-unmatch terraform/.terraform" --prune-empty -- --all

- Force-pushed the cleaned repository history to GitHub.

### Learning and Prevention

- Terraform working directories and provider binaries must never be committed.
- .gitignore should be configured before the first commit in infrastructure repositories.
- When large files are committed, rewriting Git history may be required to fully resolve the issue.

## Issue 2: VM deployment failed due to SKU capacity restriction

### Symptoms
- Terraform apply failed with error:
  `SkuNotAvailable: Standard_B2s is currently not available in eastus`
- Azure returned HTTP 409 Conflict during VM creation

### Impact
- Virtual Machine could not be provisioned
- Monitoring pipeline setup was blocked until compute was available

### Root Cause
- Azure enforces regional capacity limits on VM SKUs
- The requested VM size was temporarily unavailable in the selected region

### Resolution
- Updated VM size to an alternative SKU (`Standard_DS1_v2`) with available capacity
- Re-applied Terraform successfully without changing region

### Learning and Prevention
- Azure VM SKU availability can vary by region and time
- Terraform configurations should allow flexibility in VM sizing
- Production deployments should validate SKU availability early


## Issue 3: Diagnostic setting failed due to unsupported log category

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest
- Error message indicated that the 'Security' diagnostic category is not supported for the VM resource

### Impact
- Diagnostic settings could not be applied to the virtual machine
- Log ingestion into Log Analytics was partially blocked

### Root Cause
- Azure diagnostic categories are resource-specific
- The 'Security' category is not supported for Microsoft.Compute virtual machines
- VM security signals are provided via Defender for Cloud and Sentinel, not VM diagnostics

### Resolution
- Removed the unsupported 'Security' log category from the diagnostic settings
- Retained supported categories such as 'Administrative' and 'ServiceHealth'
- Re-applied Terraform successfully

### Learning and Prevention
- Always validate supported diagnostic categories per Azure resource type
- Security monitoring for VMs should leverage Defender for Cloud and Sentinel
- Diagnostic configurations must be tailored per resource, not generalized


## Issue 4: VM diagnostic settings failed due to unsupported log categories

### Symptoms
- Terraform apply failed with HTTP 400 BadRequest
- Azure rejected diagnostic categories such as 'Administrative' for the VM resource

### Impact
- Diagnostic settings could not be applied to the virtual machine
- Required clarification on where VM-related logs originate

### Root Cause
- Azure Virtual Machines do not support most platform log categories at the resource level
- Control-plane logs (Administrative, Policy, ServiceHealth) are emitted at the subscription or resource group level via AzureActivity
- VM diagnostic settings primarily support metrics, not logs

### Resolution
- Updated diagnostic settings to enable only supported VM metrics (`AllMetrics`)
- Relied on AzureActivity table in Log Analytics for control-plane visibility

### Learning and Prevention
- Diagnostic category support varies significantly by Azure resource type
- Logs and metrics have different scopes and ingestion paths in Azure Monitor
- Monitoring designs must account for resource-level vs subscription-level telemetry


## Issue 5: VM and Log Analytics appeared disconnected

### Symptoms
- VM and Log Analytics Workspace were created successfully
- No logs appeared in Log Analytics related to VM activity
- Monitoring appeared incomplete despite diagnostic settings

### Root Cause
- VM diagnostic settings only send metrics, not control-plane logs
- AzureActivity logs originate at the subscription scope
- Subscription-level diagnostic settings were missing

### Resolution
- Added subscription-level diagnostic settings
- Routed AzureActivity logs to the Log Analytics workspace
- Validated ingestion using KQL queries

### Learning and Prevention
- Azure Monitor uses multiple telemetry pipelines
- Control-plane logs must be enabled at subscription or resource group level
- VM observability requires combining metrics, platform logs, and guest logs


### Final Observation
- AzureActivity logs began appearing after an ingestion delay of several minutes.
- No configuration changes were required after validation.

**Conclusion:**  
Initial absence of AzureActivity logs was due to expected Azure Monitor ingestion latency, not misconfiguration.
