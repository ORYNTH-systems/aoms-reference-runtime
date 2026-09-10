from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    REAUTHORIZE = "REAUTHORIZE"


class BoundaryClass(str, Enum):
    OPERATIONAL = "OPERATIONAL"
    AUTHORITY = "AUTHORITY"
    IDENTITY = "IDENTITY"
    PERSONAL = "PERSONAL"
    PSYCHOLOGICAL = "PSYCHOLOGICAL"
    THERAPEUTIC = "THERAPEUTIC"
    SAFETY = "SAFETY"


@dataclass(frozen=True)
class AuthorityArtifact:
    authorization_id: str
    actor_id: str
    authorized_action: str
    authorized_at: str
    expires_at: str
    authority_valid: bool
    identity_state: str
    policy_version: str
    dependency_state: str
    resource_state: str
    environment_state: str
    evidence_state: str
    issuer_id: str = "legacy-authority"
    artifact_version: str = "1"


@dataclass(frozen=True)
class ExecutionContext:
    actor_id: str
    requested_action: str
    attempted_at: str
    authority_valid: bool
    identity_state: str
    policy_version: str
    dependency_state: str
    resource_state: str
    environment_state: str
    evidence_state: str
    boundary_signals: List[str] = field(default_factory=list)
    context_id: str = ""


@dataclass(frozen=True)
class AuthorityState:
    reconstructed: bool
    effective: bool
    reasons: List[str]
    provenance: List[str]


@dataclass(frozen=True)
class ContinuityVector:
    dimensions: Dict[str, bool]
    violations: List[str]
    continuous: bool
    provenance: List[str]


@dataclass(frozen=True)
class BoundaryAssessment:
    crossed: bool
    classes: List[str]
    signals: List[str]
    requires_escalation: bool
    provenance: List[str]


@dataclass(frozen=True)
class ReconciliationRecord:
    required: bool
    resolved: bool
    violations: List[str]
    disposition: str
    provenance: List[str]


@dataclass(frozen=True)
class EligibilityRecord:
    eligible: bool
    reasons: List[str]
    proof_complete: bool
    provenance: List[str]


@dataclass(frozen=True)
class GovernanceState:
    authority: AuthorityState
    continuity: ContinuityVector
    boundary: BoundaryAssessment
    reconciliation: ReconciliationRecord
    eligibility: EligibilityRecord


@dataclass(frozen=True)
class ExecutionDecision:
    execution_id: str
    decision: Decision
    terminal: bool
    reasons: List[str]
    governance: GovernanceState
    provenance: List[str]
    runtime_version: str = "2.0.0"

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["decision"] = self.decision.value
        return value
