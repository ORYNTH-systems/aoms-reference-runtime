from collections import Counter


def generate_metrics(results):
    total_cases = len(results)
    total_declined = sum(1 for r in results if r["execution_result"] == "DECLINED")
    total_approved = sum(1 for r in results if r["execution_result"] == "APPROVED")
    total_admissible = sum(1 for r in results if r["admissibility"] is True)
    total_inadmissible = sum(1 for r in results if r["admissibility"] is False)

    violation_counter = Counter()

    for result in results:
        for violation in result["violations"]:
            violation_counter[violation] += 1

    return {
        "total_cases": total_cases,
        "total_approved": total_approved,
        "total_declined": total_declined,
        "total_admissible": total_admissible,
        "total_inadmissible": total_inadmissible,
        "violation_counts": dict(violation_counter)
    }


def print_metrics(metrics):
    print("")
    print("AOMS Metrics")
    print(f"Total Cases: {metrics['total_cases']}")
    print(f"Approved Executions: {metrics['total_approved']}")
    print(f"Declined Executions: {metrics['total_declined']}")
    print(f"Admissible Cases: {metrics['total_admissible']}")
    print(f"Inadmissible Cases: {metrics['total_inadmissible']}")

    print("")
    print("Violation Frequency")

    for violation, count in sorted(metrics["violation_counts"].items()):
        print(f"{violation}: {count}")
