import argparse
import glob

from case_loader import load_case
from reconciliation import reconcile
from execution import execute
from evidence import write_evidence
from metrics import generate_metrics, print_metrics


def run_case(path):
    case_id, description, authorized, current = load_case(path)

    reconciliation = reconcile(
        authorized,
        current
    )

    execution_result = execute(
        authorized,
        current
    )

    result = {
        "case_id": case_id,
        "description": description,
        "violations": reconciliation.violations,
        "admissibility": reconciliation.admissibility,
        "execution_result": execution_result
    }

    artifact = write_evidence(result)

    print(f"Case: {case_id}")
    print(f"Description: {description}")
    print(f"Violations: {reconciliation.violations}")
    print(f"Admissibility: {reconciliation.admissibility}")
    print(f"Execution Result: {execution_result}")
    print(f"Evidence Artifact: {artifact}")
    print("")

    return result


def run_all_cases():
    paths = sorted(
        glob.glob("cases/AOMS-*.json")
    )

    results = []

    for path in paths:
        results.append(
            run_case(path)
        )

    metrics = generate_metrics(results)
    print_metrics(metrics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AOMS reference runtime"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all AOMS cases"
    )

    parser.add_argument(
        "--case",
        default="cases/AOMS-001.json",
        help="Path to a single AOMS case JSON file"
    )

    args = parser.parse_args()

    if args.all:
        run_all_cases()
    else:
        run_case(args.case)
