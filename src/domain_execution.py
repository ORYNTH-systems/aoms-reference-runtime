import argparse
import csv
import glob
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

from canonical.models import AuthorityArtifact, ExecutionContext
from canonical.pipeline import CanonicalPipeline

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_case(path):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data, AuthorityArtifact(**data["artifact"]), ExecutionContext(**data["context"])


def run_case(path):
    data, artifact, context = load_case(path)
    result = CanonicalPipeline().evaluate(artifact, context)
    expected = data["expected"]
    reasons_present = all(reason in result.reasons for reason in expected["required_reasons"])
    passed = (
        result.decision.value == expected["decision"]
        and result.terminal is expected["terminal"]
        and result.governance.eligibility.proof_complete is expected["proof_complete"]
        and reasons_present
        and "decision_engine" in result.provenance
        and result.execution_id in result.provenance
    )
    return {
        "case_id": data["case_id"],
        "domain": data["domain"],
        "effect_class": data["effect_class"],
        "proof_obligation": data["proof_obligation"],
        "expected_decision": expected["decision"],
        "actual_decision": result.decision.value,
        "required_reasons": expected["required_reasons"],
        "actual_reasons": result.reasons,
        "terminal": result.terminal,
        "proof_complete": result.governance.eligibility.proof_complete,
        "execution_id": result.execution_id,
        "provenance": result.provenance,
        "passed": passed,
    }


def write_json(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def run_all(write_reports=True):
    paths = sorted(glob.glob(os.path.join(ROOT, "cases", "domains", "AOMS-B06-*.json")))
    results = [run_case(path) for path in paths]
    decision_counts = Counter(item["actual_decision"] for item in results)
    domain_counts = Counter(item["domain"] for item in results)
    report = {
        "suite": "AOMS Batch 07 domain execution proof wave",
        "schema_version": "3.0.0",
        "case_count": len(results),
        "passed": sum(item["passed"] for item in results),
        "failed": sum(not item["passed"] for item in results),
        "decision_counts": dict(sorted(decision_counts.items())),
        "domain_counts": dict(sorted(domain_counts.items())),
        "status": "EXECUTION-VERIFIED" if results and all(item["passed"] for item in results) else "FAILED",
        "results": results,
    }
    if write_reports:
        report_root = os.path.join(ROOT, "reports", "domain-execution")
        write_json(os.path.join(report_root, "BATCH_07_AGGREGATE.json"), report)
        grouped = defaultdict(list)
        for item in results:
            grouped[item["domain"]].append(item)
        for domain, items in sorted(grouped.items()):
            domain_report = {
                "domain": domain,
                "case_count": len(items),
                "passed": sum(item["passed"] for item in items),
                "failed": sum(not item["passed"] for item in items),
                "status": "EXECUTION-VERIFIED" if all(item["passed"] for item in items) else "FAILED",
                "results": items,
            }
            write_json(os.path.join(report_root, domain + ".json"), domain_report)
        registry_path = os.path.join(ROOT, "registries", "AOMS-RG-025_DOMAIN_EXECUTION_REGISTRY.csv")
        with open(registry_path, "r", encoding="utf-8", newline="") as handle:
            registry_rows = list(csv.DictReader(handle))
        passed_ids = {item["case_id"] for item in results if item["passed"]}
        with open(registry_path, "w", encoding="utf-8", newline="") as handle:
            fieldnames = ["case_id", "domain", "effect_class", "expected_decision", "proof_obligation", "status"]
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in registry_rows:
                row["status"] = "EXECUTION-VERIFIED" if row["case_id"] in passed_ids else "FAILED"
                writer.writerow(row)
        freeze_paths = paths + [
            os.path.join(report_root, name)
            for name in ["BATCH_07_AGGREGATE.json"] + [domain + ".json" for domain in sorted(grouped)]
        ] + [registry_path]
        manifest = os.path.join(report_root, "SHA256SUMS.txt")
        with open(manifest, "w", encoding="utf-8", newline="\n") as handle:
            for item_path in freeze_paths:
                with open(item_path, "rb") as source:
                    digest = hashlib.sha256(source.read()).hexdigest()
                handle.write(digest + "  " + os.path.relpath(item_path, ROOT).replace(os.sep, "/") + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description="Execute all Batch 07 domain fixtures")
    parser.parse_args()
    report = run_all(write_reports=True)
    summary = {key: value for key, value in report.items() if key != "results"}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if report["case_count"] == 60 and report["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
