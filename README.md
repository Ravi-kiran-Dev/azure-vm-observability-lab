# Azure VM Observability Lab

## Overview
This project demonstrates a hands-on implementation of Azure infrastructure monitoring and observability using **Terraform**, **KQL**, and **Python**.

The goal is to design a production-like monitoring setup for Azure Virtual Machines, focusing on:
- Proactive detection of issues
- Actionable insights using KQL
- Infrastructure-as-Code for repeatability
- Automation and log analysis using Python

This project is intentionally built step-by-step to reflect real-world engineering workflows, including challenges faced and how they were resolved.

---

## Architecture (High Level)
- Azure Resource Group
- Log Analytics Workspace
- Azure Virtual Machine
- Diagnostic Settings → Log Analytics
- KQL Dashboards & Alerts
- Python-based Log Analytics querying

---

## Key Technologies Used
- **Azure Monitor & Log Analytics**
- **Kusto Query Language (KQL)**
- **Terraform**
- **Python**
- **Azure CLI**

---

## Project Phases
1. Environment & monitoring foundation using Terraform
2. VM provisioning with diagnostics enabled
3. KQL queries for infrastructure health and failures
4. Alerting using log-based rules
5. Python automation for log analysis and enrichment

---

## Troubleshooting & Learnings
Real-world issues encountered during the build and their resolutions are documented here:
- [Issues and Fixes](docs/issues-and-fixes.md)
- [Key Learnings](docs/learnings.md)

---

## Why This Project?
This project is designed to reflect how monitoring is implemented in real enterprise environments—balancing visibility, performance, and cost—rather than being a simple demo or tutorial.
