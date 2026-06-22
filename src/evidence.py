import json
import os


def write_evidence(result, output_dir="reports/json"):

    os.makedirs(output_dir, exist_ok=True)

    filename = f"{result['case_id']}.json"

    path = os.path.join(
        output_dir,
        filename
    )

    with open(path, "w") as f:
        json.dump(
            result,
            f,
            indent=2
        )

    return path
