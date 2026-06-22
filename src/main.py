from models import AuthorizedState, CurrentState
from execution import execute


authorized = AuthorizedState(
    authorization_id="AOMS-001",
    actor_id="vendor-123",
    authorized_action="process_payment",
    authorized_at="2026-06-22T10:00:00",
    expires_at="2026-06-23T10:00:00",
    authority_valid=True,
    policy_version="1.0",
    dependency_state="active",
    resource_state="available",
    environment_state="normal"
)

current = CurrentState(
    actor_id="vendor-123",
    current_action="process_payment",
    execution_attempted_at="2026-06-22T12:00:00",
    authority_valid=True,
    policy_version="1.0",
    dependency_state="active",
    resource_state="available",
    environment_state="normal"
)

result = execute(
    authorized,
    current
)

print(f"Execution Result: {result}")
