"""Deterministically generate the AOMS Phase II 250-case proof wave."""
import copy
import csv
import json
import os
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CASE_DIR = os.path.join(ROOT, "cases", "canonical")
REGISTRY = os.path.join(ROOT, "registries", "AOMS-RG-022_CANONICAL_CASE_REGISTRY.csv")

BASE_ARTIFACT = {
    "authorization_id": "AUTH-CANONICAL-001", "actor_id": "agent-alpha",
    "authorized_action": "execute-governed-transition", "authorized_at": "2026-01-01T00:00:00Z",
    "expires_at": "2027-01-01T00:00:00Z", "authority_valid": True,
    "identity_state": "identity-bound", "policy_version": "policy-v1",
    "dependency_state": "ready", "resource_state": "available",
    "environment_state": "valid", "evidence_state": "sufficient",
    "issuer_id": "principal-alpha", "artifact_version": "2"
}
BASE_CONTEXT = {
    "actor_id": "agent-alpha", "requested_action": "execute-governed-transition",
    "attempted_at": "2026-06-01T00:00:00Z", "authority_valid": True,
    "identity_state": "identity-bound", "policy_version": "policy-v1",
    "dependency_state": "ready", "resource_state": "available",
    "environment_state": "valid", "evidence_state": "sufficient",
    "boundary_signals": [], "context_id": ""
}

REAUTHORIZE = [
    ("artifact-authority-invalid", "authority_invalid", lambda a, c: a.update(authority_valid=False)),
    ("context-authority-invalid", "authority_invalid", lambda a, c: c.update(authority_valid=False)),
    ("authorization-expired", "authorization_expired", lambda a, c: c.update(attempted_at="2028-01-01T00:00:00Z")),
    ("execution-too-early", "execution_too_early", lambda a, c: c.update(attempted_at="2025-01-01T00:00:00Z")),
    ("actor-mismatch", "actor_mismatch", lambda a, c: c.update(actor_id="agent-unknown")),
    ("action-drift", "action_drift_detected", lambda a, c: c.update(requested_action="execute-unbound-transition")),
    ("identity-discontinuity", "identity_continuity_failed", lambda a, c: c.update(identity_state="identity-changed")),
    ("policy-change", "policy_changed", lambda a, c: c.update(policy_version="policy-v2")),
]
DENY = [
    ("dependency-change", "dependency_state_changed", lambda a, c: c.update(dependency_state="failed")),
    ("resource-loss", "resource_unavailable", lambda a, c: c.update(resource_state="unavailable")),
    ("environment-change", "environment_invalid", lambda a, c: c.update(environment_state="invalid")),
    ("evidence-change", "evidence_insufficient", lambda a, c: c.update(evidence_state="insufficient")),
    ("operational-boundary", "boundary_crossed:operational", lambda a, c: c.update(boundary_signals=["OPERATIONAL"])),
    ("authority-boundary", "boundary_crossed:authority", lambda a, c: c.update(boundary_signals=["AUTHORITY"])),
    ("identity-boundary", "boundary_crossed:identity", lambda a, c: c.update(boundary_signals=["IDENTITY"])),
]
ESCALATE = [
    ("personal-boundary", "boundary_crossed:personal", lambda a, c: c.update(boundary_signals=["PERSONAL"])),
    ("psychological-boundary", "boundary_crossed:psychological", lambda a, c: c.update(boundary_signals=["PSYCHOLOGICAL"])),
    ("therapeutic-boundary", "boundary_crossed:therapeutic", lambda a, c: c.update(boundary_signals=["THERAPEUTIC"])),
    ("safety-boundary", "boundary_crossed:safety", lambda a, c: c.update(boundary_signals=["SAFETY"])),
    ("unknown-boundary", "boundary_crossed:unknown", lambda a, c: c.update(boundary_signals=["UNREGISTERED-BOUNDARY"])),
    ("compound-personal-safety", "boundary_crossed:personal", lambda a, c: c.update(boundary_signals=["PERSONAL", "SAFETY"])),
    ("compound-therapeutic-psychological", "boundary_crossed:psychological", lambda a, c: c.update(boundary_signals=["THERAPEUTIC", "PSYCHOLOGICAL"])),
]

def build_case(number, family, variant, expected, reason, mutate=None):
    artifact = copy.deepcopy(BASE_ARTIFACT)
    context = copy.deepcopy(BASE_CONTEXT)
    case_id = "AOMS-%03d" % number
    artifact["authorization_id"] = "AUTH-%03d" % number
    context["context_id"] = "CTX-%03d" % number
    if mutate:
        mutate(artifact, context)
    return {
        "case_id": case_id, "schema_version": "2.0.0", "family": family,
        "variant": variant, "description": "%s canonical proof %03d" % (variant.replace("-", " "), number),
        "artifact": artifact, "context": context,
        "expected": {"decision": expected, "required_reasons": [reason] if reason else [], "terminal": True}
    }

def generate():
    cases = []
    for number in range(101, 126):
        cases.append(build_case(number, "ALLOW", "continuous-authorized-state-%02d" % (number - 100), "ALLOW", None))
    for offset, number in enumerate(range(126, 201)):
        variant, reason, mutate = REAUTHORIZE[offset % len(REAUTHORIZE)]
        cases.append(build_case(number, "REAUTHORIZE", variant, "REAUTHORIZE", reason, mutate))
    for offset, number in enumerate(range(201, 276)):
        variant, reason, mutate = DENY[offset % len(DENY)]
        cases.append(build_case(number, "DENY", variant, "DENY", reason, mutate))
    for offset, number in enumerate(range(276, 351)):
        variant, reason, mutate = ESCALATE[offset % len(ESCALATE)]
        cases.append(build_case(number, "ESCALATE", variant, "ESCALATE", reason, mutate))
    assert len(cases) == 250
    assert Counter(item["expected"]["decision"] for item in cases) == Counter({"ALLOW": 25, "REAUTHORIZE": 75, "DENY": 75, "ESCALATE": 75})
    os.makedirs(CASE_DIR, exist_ok=True)
    expected_names = set()
    for item in cases:
        name = item["case_id"] + ".json"
        expected_names.add(name)
        with open(os.path.join(CASE_DIR, name), "w", encoding="utf-8", newline="\n") as handle:
            json.dump(item, handle, indent=2, sort_keys=True)
            handle.write("\n")
    actual_names = {name for name in os.listdir(CASE_DIR) if name.endswith(".json")}
    if actual_names != expected_names:
        raise RuntimeError("canonical case directory contains an unexpected JSON boundary")
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["case_id", "family", "variant", "expected_decision", "required_reasons", "schema_version"])
        for item in cases:
            writer.writerow([item["case_id"], item["family"], item["variant"], item["expected"]["decision"], ";".join(item["expected"]["required_reasons"]), item["schema_version"]])
    return cases

if __name__ == "__main__":
    generated = generate()
    print("GENERATED: %d canonical cases" % len(generated))
    print("RANGE: AOMS-101 through AOMS-350")
    print("DISTRIBUTION: ALLOW=25 DENY=75 ESCALATE=75 REAUTHORIZE=75")
