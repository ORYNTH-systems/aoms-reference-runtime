import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cases" / "collective"


def artifact(actor, action="collective-act"):
    return {
        "authorization_id": "AUTH-" + actor,
        "actor_id": actor,
        "authorized_action": action,
        "authorized_at": "2026-01-01T00:00:00Z",
        "expires_at": "2027-01-01T00:00:00Z",
        "authority_valid": True,
        "identity_state": "VERIFIED",
        "policy_version": "COLLECTIVE-1",
        "dependency_state": "READY",
        "resource_state": "READY",
        "environment_state": "VALID",
        "evidence_state": "SUFFICIENT",
        "issuer_id": "principal-001",
        "artifact_version": "1",
    }


def context(actor, action="collective-act"):
    return {
        "actor_id": actor,
        "requested_action": action,
        "attempted_at": "2026-06-01T00:00:00Z",
        "authority_valid": True,
        "identity_state": "VERIFIED",
        "policy_version": "COLLECTIVE-1",
        "dependency_state": "READY",
        "resource_state": "READY",
        "environment_state": "VALID",
        "evidence_state": "SUFFICIENT",
        "boundary_signals": [],
        "context_id": "CTX-" + actor,
    }


def participant(actor, role, required=True):
    return {
        "participant_id": actor,
        "role": role,
        "required": required,
        "artifact": artifact(actor),
        "context": context(actor),
        "delegated_scope": ["collective-act"],
        "delegation_chain": [],
    }


def request(case_id):
    return {
        "request_id": case_id + "-REQUEST",
        "requested_action": "collective-act",
        "coordinator_id": "coordinator-001",
        "coordinator_authorized": True,
        "required_roles": ["PROPOSER", "APPROVER"],
        "quorum_required": 2,
        "participants": [participant("agent-001", "PROPOSER"), participant("agent-002", "APPROVER")],
        "separation_of_duties": [["PROPOSER", "APPROVER"]],
    }


def case(number, mutate, decision, reasons):
    case_id = f"AOMS-COL-{number:03d}"
    body = request(case_id)
    mutate(body)
    return {"case_id": case_id, "request": body, "expected": {"decision": decision, "required_reasons": reasons}}


def no_change(body):
    return None


def generate():
    cases = []
    cases.append(case(1, no_change, "ALLOW", []))
    cases.append(case(2, lambda body: body.update(required_roles=["PROPOSER", "APPROVER", "AUDITOR"]), "DENY", ["required_role_missing:AUDITOR"]))
    cases.append(case(3, lambda body: body.update(coordinator_authorized=False), "REAUTHORIZE", ["coordinator_unauthorized"]))
    cases.append(case(4, lambda body: body["participants"][1].update(delegated_scope=["read-only"]), "DENY", ["participant_scope_insufficient"]))
    cases.append(case(5, lambda body: body.update(quorum_required=3), "DENY", ["quorum_not_satisfied"]))

    def duplicate(body):
        body["participants"][1]["participant_id"] = "agent-001"
    cases.append(case(6, duplicate, "DENY", ["duplicate_participant_identity"]))

    def duty_failure(body):
        body["participants"][1]["participant_id"] = "agent-001"
    cases.append(case(7, duty_failure, "DENY", ["separation_of_duties_violated"]))

    def expire(body):
        body["participants"][1]["context"]["attempted_at"] = "2028-01-01T00:00:00Z"
    cases.append(case(8, expire, "REAUTHORIZE", ["authorization_expired"]))

    def boundary(body):
        body["participants"][1]["context"]["boundary_signals"] = ["PERSONAL"]
    cases.append(case(9, boundary, "ESCALATE", ["boundary_crossed:personal"]))

    def optional_invalid(body):
        extra = participant("agent-003", "OBSERVER", False)
        extra["context"]["dependency_state"] = "FAILED"
        body["participants"].append(extra)
    cases.append(case(10, optional_invalid, "ALLOW", []))

    def revoked(body):
        body["participants"][1]["delegation_chain"] = [{
            "delegator_id": "principal-001", "delegate_id": "agent-002",
            "scope": ["collective-act"], "active": True, "revoked": True,
        }]
    cases.append(case(11, revoked, "DENY", ["delegation_inactive"]))

    def disconnected(body):
        body["participants"][1]["delegation_chain"] = [
            {"delegator_id": "principal-001", "delegate_id": "middle-001", "scope": ["collective-act"], "active": True, "revoked": False},
            {"delegator_id": "other-001", "delegate_id": "agent-002", "scope": ["collective-act"], "active": True, "revoked": False},
        ]
    cases.append(case(12, disconnected, "DENY", ["delegation_chain_disconnected"]))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for old in OUTPUT.glob("AOMS-COL-*.json"):
        old.unlink()
    for item in cases:
        path = OUTPUT / (item["case_id"] + ".json")
        path.write_text(json.dumps(item, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"GENERATED: {len(cases)} collective authority cases")


if __name__ == "__main__":
    generate()
