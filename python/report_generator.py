# report_generator.py
from query_azure_activity import get_failed_operations
from vm_metrics_report import get_vm_cpu_metrics


def generate_report():
    print("=== Azure Observability Report ===")

    failures = get_failed_operations()
    print("\nFailed Operations:")
    print(failures if failures else "No failures detected")

    cpu = get_vm_cpu_metrics()
    print("\nRecent CPU Metrics:")
    print(cpu[:5])


if __name__ == "__main__":
    generate_report()
