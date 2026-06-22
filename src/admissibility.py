from reconciliation import reconcile
from models import AuthorizedState, CurrentState


def determine_admissibility(
    authorized: AuthorizedState,
    current: CurrentState
) -> bool:
    result = reconcile(authorized, current)
    return result.admissibility
