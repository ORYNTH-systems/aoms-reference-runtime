import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from canonical.collective_pipeline import CollectiveAuthorityPipeline
from collective_cases import load_collective_case


def evaluate():
    paths = sorted((ROOT / "cases" / "collective").glob("AOMS-COL-*.json"))
    errors = []
    counts = Counter()
    for path in paths:
        case_id, request, expected = load_collective_case(path)
        first = CollectiveAuthorityPipeline().evaluate(request)
        second = CollectiveAuthorityPipeline().evaluate(request)
        counts[first.decision.value] += 1
        if first.decision.value != expected["decision"]:
            errors.append(f"{case_id}: expected {expected['decision']}; found {first.decision.value}")
        for reason in expected.get("required_reasons", []):
            if reason not in first.reasons and not any(reason in item.reasons for item in first.participants):
                errors.append(f"{case_id}: missing reason {reason}")
        if not first.terminal:
            errors.append(f"{case_id}: nonterminal")
        if first.execution_id == second.execution_id:
            errors.append(f"{case_id}: execution identity reused")
        if first.execution_id not in first.provenance:
            errors.append(f"{case_id}: incomplete provenance")
    report = {
        "profile": "AOMS-COLLECTIVE-001",
        "case_count": len(paths),
        "decision_counts": dict(sorted(counts.items())),
        "checks": {
            "exact_case_count": len(paths) == 12,
            "all_cases_pass": not errors,
            "all_decisions_represented": set(counts) == {"ALLOW", "DENY", "ESCALATE", "REAUTHORIZE"},
            "fresh_execution_identity": not any("identity reused" in item for item in errors),
            "terminal_and_provenanced": not any("nonterminal" in item or "provenance" in item for item in errors),
        },
        "errors": errors,
    }
    report["passed"] = all(report["checks"].values())
    return report


if __name__ == "__main__":
    result = evaluate()
    output = ROOT / "reports" / "collective" / "BATCH_12_COLLECTIVE_AUTHORITY.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
