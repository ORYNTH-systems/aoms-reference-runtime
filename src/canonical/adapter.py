from models import AuthorizedState, CurrentState

from .models import AuthorityArtifact, ExecutionContext, ExecutionDecision
from .pipeline import CanonicalPipeline


def adapt_v1(authorized: AuthorizedState, current: CurrentState):
    artifact = AuthorityArtifact(
        authorization_id=authorized.authorization_id,
        actor_id=authorized.actor_id,
        authorized_action=authorized.authorized_action,
        authorized_at=authorized.authorized_at,
        expires_at=authorized.expires_at,
        authority_valid=authorized.authority_valid,
        identity_state=authorized.identity_state,
        policy_version=authorized.policy_version,
        dependency_state=authorized.dependency_state,
        resource_state=authorized.resource_state,
        environment_state=authorized.environment_state,
        evidence_state=authorized.evidence_state,
    )
    context = ExecutionContext(
        actor_id=current.actor_id,
        requested_action=current.current_action,
        attempted_at=current.execution_attempted_at,
        authority_valid=current.authority_valid,
        identity_state=current.identity_state,
        policy_version=current.policy_version,
        dependency_state=current.dependency_state,
        resource_state=current.resource_state,
        environment_state=current.environment_state,
        evidence_state=current.evidence_state,
    )
    return artifact, context


def evaluate_v1(authorized: AuthorizedState, current: CurrentState) -> ExecutionDecision:
    artifact, context = adapt_v1(authorized, current)
    return CanonicalPipeline().evaluate(artifact, context)


def legacy_execution_result(result: ExecutionDecision) -> str:
    return "APPROVED" if result.decision.value == "ALLOW" else "DECLINED"
