from admissibility import determine_admissibility
from models import AuthorizedState, CurrentState


def execute(
    authorized: AuthorizedState,
    current: CurrentState
) -> str:

    admissible = determine_admissibility(
        authorized,
        current
    )

    if admissible:
        return "APPROVED"

    return "DECLINED"
