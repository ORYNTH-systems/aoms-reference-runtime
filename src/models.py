from dataclasses import dataclass
from typing import List


@dataclass
class AuthorizedState:
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


@dataclass
class CurrentState:
    actor_id: str
    current_action: str
    execution_attempted_at: str
    authority_valid: bool
    identity_state: str
    policy_version: str
    dependency_state: str
    resource_state: str
    environment_state: str
    evidence_state: str


@dataclass
class ReconciliationResult:
    reconciliation_required: bool
    violations: List[str]
    admissibility: bool


@dataclass
class ExecutionResult:
    result: str
