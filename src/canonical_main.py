import argparse
import json

from canonical.adapter import adapt_v1
from canonical.pipeline import CanonicalPipeline
from case_loader import load_case


def main() -> int:
    parser = argparse.ArgumentParser(description="AOMS Phase II canonical runtime")
    parser.add_argument("--case", default="cases/AOMS-001.json")
    parser.add_argument("--boundary", action="append", default=[], help="Agent-readable boundary class")
    args = parser.parse_args()
    _, _, authorized, current = load_case(args.case)
    artifact, context = adapt_v1(authorized, current)
    if args.boundary:
        from dataclasses import replace
        context = replace(context, boundary_signals=args.boundary)
    result = CanonicalPipeline().evaluate(artifact, context)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.decision.value == "ALLOW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
