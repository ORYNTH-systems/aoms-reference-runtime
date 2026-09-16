import argparse
import glob
import json
import os
import sys
from collections import Counter

from canonical.models import AuthorityArtifact, ExecutionContext
from canonical.pipeline import CanonicalPipeline

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_canonical_case(path):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data, AuthorityArtifact(**data["artifact"]), ExecutionContext(**data["context"])

def run_case(path):
    data, artifact, context = load_canonical_case(path)
    result = CanonicalPipeline().evaluate(artifact, context)
    expected = data["expected"]
    reasons_present = all(reason in result.reasons for reason in expected["required_reasons"])
    passed = result.decision.value == expected["decision"] and result.terminal == expected["terminal"] and reasons_present
    return {"case_id": data["case_id"], "family": data["family"], "variant": data["variant"],
            "expected_decision": expected["decision"], "actual_decision": result.decision.value,
            "required_reasons": expected["required_reasons"], "actual_reasons": result.reasons,
            "terminal": result.terminal, "proof_complete": result.governance.eligibility.proof_complete,
            "passed": passed}

def run_all(output=None):
    paths = sorted(glob.glob(os.path.join(ROOT, "cases", "canonical", "AOMS-*.json")))
    results = [run_case(path) for path in paths]
    report = {"suite": "AOMS Phase II canonical proof wave", "schema_version": "2.0.0",
              "case_count": len(results), "passed": sum(item["passed"] for item in results),
              "failed": sum(not item["passed"] for item in results),
              "decision_counts": dict(sorted(Counter(item["actual_decision"] for item in results).items())),
              "results": results}
    if output:
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return report

def main():
    parser = argparse.ArgumentParser(description="Run AOMS canonical cases")
    parser.add_argument("--case")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output", default=os.path.join(ROOT, "reports", "canonical", "BATCH_03_RESULTS.json"))
    args = parser.parse_args()
    if args.all:
        report = run_all(args.output)
        print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2, sort_keys=True))
        return 0 if report["failed"] == 0 else 1
    if not args.case:
        parser.error("--case or --all is required")
    result = run_case(args.case)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    sys.exit(main())
