from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from .models import AuthorityArtifact, Decision, ExecutionContext


@dataclass(frozen=True)
class DelegationLink:
    delegator_id: str
    delegate_id: str
    scope: List[str]
    active: bool = True
    revoked: bool = False


@dataclass(frozen=True)
class CollectiveParticipant:
    participant_id: str
    role: str
    required: bool
    artifact: AuthorityArtifact
    context: ExecutionContext
    delegated_scope: List[str]
    delegation_chain: List[DelegationLink] = field(default_factory=list)


@dataclass(frozen=True)
class CollectiveExecutionRequest:
    request_id: str
    requested_action: str
    coordinator_id: str
    coordinator_authorized: bool
    required_roles: List[str]
    quorum_required: int
    participants: List[CollectiveParticipant]
    separation_of_duties: List[List[str]] = field(default_factory=list)


@dataclass(frozen=True)
class ParticipantEvaluation:
    participant_id: str
    role: str
    required: bool
    decision: Decision
    admissible: bool
    delegation_valid: bool
    scope_valid: bool
    reasons: List[str]
    provenance: List[str]


@dataclass(frozen=True)
class CollectiveDecision:
    execution_id: str
    request_id: str
    decision: Decision
    terminal: bool
    reasons: List[str]
    participants: List[ParticipantEvaluation]
    provenance: List[str]
    runtime_version: str = "3.0.0-phase-iii"

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["decision"] = self.decision.value
        for participant in value["participants"]:
            participant["decision"] = participant["decision"].value
        return value
