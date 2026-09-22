import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "benchmarks" / "AOMS-BENCH-001_DOMAIN_MATRIX.csv"
OUTPUT = ROOT / "cases" / "domains"
REGISTRY = ROOT / "registries" / "AOMS-RG-025_DOMAIN_EXECUTION_REGISTRY.csv"


def build_case(row):
    scenario_id = row["scenario_id"]
    domain = row["domain"]
    decision = row["expected_decision"]
    action = row["effect_class"].replace(" ", "_")
    artifact = {
        "authorization_id": "AUTH-" + scenario_id,
        "actor_id": "actor-" + domain.lower(),
        "authorized_action": action,
        "authorized_at": "2026-01-01T00:00:00Z",
        "expires_at": "2027-01-01T00:00:00Z",
        "authority_valid": True,
        "identity_state": "VERIFIED",
        "policy_version": "AOMS-DOMAIN-1",
        "dependency_state": "READY",
        "resource_state": "AVAILABLE",
        "environment_state": "VALID",
        "evidence_state": "SUFFICIENT",
        "issuer_id": "orynth-domain-authority",
        "artifact_version": "1",
    }
    context = {
        "actor_id": artifact["actor_id"],
        "requested_action": action,
        "attempted_at": "2026-06-01T00:00:00Z",
        "authority_valid": True,
        "identity_state": "VERIFIED",
        "policy_version": "AOMS-DOMAIN-1",
        "dependency_state": "READY",
        "resource_state": "AVAILABLE",
        "environment_state": "VALID",
        "evidence_state": "SUFFICIENT",
        "boundary_signals": [],
        "context_id": "CTX-" + scenario_id,
    }
    reasons = []
    if decision == "DENY":
        context["dependency_state"] = "FAILED"
        reasons = ["dependency_state_changed"]
    elif decision == "ESCALATE":
        context["boundary_signals"] = ["SAFETY"]
        reasons = ["boundary_crossed:safety"]
    elif decision == "REAUTHORIZE":
        context["attempted_at"] = "2028-01-01T00:00:00Z"
        reasons = ["authorization_expired"]
    return {
        "schema_version": "3.0.0",
        "case_id": scenario_id,
        "domain": domain,
        "effect_class": row["effect_class"],
        "source_benchmark": "AOMS-BENCH-001",
        "source_status": row["status"],
        "proof_obligation": row["proof_obligation"],
        "artifact": artifact,
        "context": context,
        "expected": {
            "decision": decision,
            "terminal": True,
            "required_reasons": reasons,
            "proof_complete": True,
        },
    }


def main():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 60:
        raise RuntimeError("expected exactly 60 Batch 06 scenarios")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    generated = []
    for row in rows:
        data = build_case(row)
        path = OUTPUT / (data["case_id"] + ".json")
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        generated.append(data)
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["case_id", "domain", "effect_class", "expected_decision", "proof_obligation", "status"])
        for data in generated:
            writer.writerow([
                data["case_id"], data["domain"], data["effect_class"],
                data["expected"]["decision"], data["proof_obligation"], "EXECUTION-CANDIDATE",
            ])
    print("GENERATED: 60 domain execution fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
