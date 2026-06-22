import json

from models import AuthorizedState, CurrentState


def load_case(path):

    with open(path, "r") as f:
        data = json.load(f)

    authorized = AuthorizedState(
        **data["authorized"]
    )

    current = CurrentState(
        **data["current"]
    )

    return (
        data["case_id"],
        data["description"],
        authorized,
        current
    )
