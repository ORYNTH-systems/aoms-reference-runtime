from models import AuthorizedState, CurrentState, ReconciliationResult


def reconcile(
    authorized: AuthorizedState,
    current: CurrentState
) -> ReconciliationResult:
    violations = []

    if not current.authority_valid:
        violations.append("authority_invalid")

    if current.execution_attempted_at > authorized.expires_at:
        violations.append("authorization_expired")

    if current.current_action != authorized.authorized_action:
        violations.append("action_drift_detected")

    if current.policy_version != authorized.policy_version:
        violations.append("policy_changed")

    if current.dependency_state != authorized.dependency_state:
        violations.append("dependency_state_changed")

    if current.resource_state != authorized.resource_state:
        violations.append("resource_unavailable")

    if current.environment_state != authorized.environment_state:
        violations.append("environment_invalid")

    admissibility = len(violations) == 0

    return ReconciliationResult(
        reconciliation_required=True,
        violations=violations,
        admissibility=admissibility
    )
