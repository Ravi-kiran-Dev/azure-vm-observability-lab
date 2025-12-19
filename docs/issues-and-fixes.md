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