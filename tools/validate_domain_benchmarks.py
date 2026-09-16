import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["AI_AGENTS", "FINANCE", "HEALTHCARE", "ROBOTICS", "CIVIC_SYSTEMS", "EMERGENCY_RESPONSE"]
DECISIONS = ["ALLOW", "DENY", "ESCALATE", "REAUTHORIZE"]

def main():
    errors = []
    matrix = ROOT / "benchmarks/AOMS-BENCH-001_DOMAIN_MATRIX.csv"
    with matrix.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["scenario_id"] for row in rows]
    domain_counts = Counter(row["domain"] for row in rows)
    decision_counts = Counter(row["expected_decision"] for row in rows)
    if len(rows) != 60: errors.append("scenario_count_not_60")
    if len(ids) != len(set(ids)): errors.append("duplicate_scenario_id")
    if domain_counts != Counter({d: 10 for d in DOMAINS}): errors.append("domain_distribution_invalid")
    if decision_counts != Counter({d: 15 for d in DECISIONS}): errors.append("decision_distribution_invalid")
    for row in rows:
        for field in ("trigger", "reason_code", "engine_focus", "proof_obligation"):
            if not row[field].strip(): errors.append(f"missing_{field}:{row['scenario_id']}")
    for domain in DOMAINS:
        if not (ROOT / "case-studies" / f"{domain}.md").is_file(): errors.append(f"missing_profile:{domain}")
    registry = ROOT / "registries/AOMS-RG-024_DOMAIN_PROFILE_REGISTRY.csv"
    with registry.open(encoding="utf-8", newline="") as handle:
        profiles = list(csv.DictReader(handle))
    if len(profiles) != 6: errors.append("profile_count_not_6")
    for profile in profiles:
        if not (ROOT / profile["case_study"]).is_file(): errors.append(f"unresolved_profile:{profile['profile_id']}")
    report = {"profile":"AOMS-BENCH-001","scenario_count":len(rows),"domain_counts":dict(sorted(domain_counts.items())),"decision_counts":dict(sorted(decision_counts.items())),"errors":errors,"passed":not errors}
    output = ROOT / "reports/benchmarks/BATCH_06_DOMAIN_VALIDATION.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__": raise SystemExit(main())
