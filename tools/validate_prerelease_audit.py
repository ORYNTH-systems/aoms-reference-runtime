import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "release" / "BATCH_09_PRERELEASE_AUDIT.json"
INVENTORY = ROOT / "architecture" / "PHASE_II_ARTIFACT_INVENTORY.md"
HASHES = ROOT / "release" / "SHA256SUMS_BATCH_09.txt"

HASH_TARGETS = [
    "README.md", "ROADMAP.md", "CHANGELOG.md", "release/TECHNICAL_SUMMARY.md",
    "publications/README.md", "specifications/README.md", "registries/README.md",
    "manuals/REPRODUCIBILITY.md", "architecture/PHASE_II_ARTIFACT_INVENTORY.md",
    "tools/validate_prerelease_audit.py", "tests/test_prerelease_audit.py",
    "reports/release/BATCH_09_PRERELEASE_AUDIT.json",
]

def count(pattern):
    return len(list(ROOT.glob(pattern)))

def validate(write_outputs=True):
    counts = {
        "v1_cases": count("cases/AOMS-*.json"),
        "canonical_cases": count("cases/canonical/AOMS-*.json"),
        "domain_cases": count("cases/domains/AOMS-B06-*.json"),
        "publications": count("publications/AOMS-*.md"),
        "specifications": count("specifications/AOMS-SPEC-*.md"),
        "registries": count("registries/AOMS-RG-*"),
    }
    counts["total_cases"] = counts["v1_cases"] + counts["canonical_cases"] + counts["domain_cases"]
    matrix = ROOT / "crosswalks" / "AOMS_CLAIM_TO_PROOF_MATRIX.csv"
    with matrix.open(encoding="utf-8", newline="") as handle:
        claims = list(csv.DictReader(handle))
    checks = {
        "v1_case_count_100": counts["v1_cases"] == 100,
        "canonical_case_count_250": counts["canonical_cases"] == 250,
        "domain_case_count_60": counts["domain_cases"] == 60,
        "total_case_count_410": counts["total_cases"] == 410,
        "claim_count_20": len(claims) == 20,
        "all_claims_execution_verified": all(row.get("proof_status") == "EXECUTION-VERIFIED" for row in claims),
        "batch_07_aggregate_present": (ROOT / "reports/domain-execution/BATCH_07_AGGREGATE.json").is_file(),
        "batch_08_closure_present": (ROOT / "reports/publications/BATCH_08_CLAIM_PROOF_VALIDATION.json").is_file(),
        "release_candidate_manifest_present": (ROOT / "release/AOMS_PHASE_II_RELEASE_CANDIDATE_MANIFEST.md").is_file(),
        "reproducibility_guide_present": (ROOT / "manuals/REPRODUCIBILITY.md").is_file(),
    }
    result = {
        "profile": "AOMS-PRERELEASE-001",
        "counts": counts,
        "closed_claims": len(claims),
        "checks": checks,
        "errors": sorted(name for name, passed in checks.items() if not passed),
        "passed": all(checks.values()),
        "release_action_performed": False,
    }
    if write_outputs:
        INVENTORY.parent.mkdir(parents=True, exist_ok=True)
        inventory = f"""# AOMS Phase II Artifact Inventory

## Verified corpus

| Surface | Count |
|---|---:|
| Preserved v1 cases | {counts['v1_cases']} |
| Canonical Phase II cases | {counts['canonical_cases']} |
| Executable domain cases | {counts['domain_cases']} |
| Total cases | {counts['total_cases']} |
| Publication manuscripts | {counts['publications']} |
| Normative specifications | {counts['specifications']} |
| Registry artifacts | {counts['registries']} |
| Closed publication claims | {len(claims)} |

## Evidence chain

The Phase II evidence chain consists of the canonical runtime, canonical cases, conformance profile, publication/specification crosswalks, six-domain benchmark design, 60 executable domain fixtures, claim-proof closure matrix, evidence appendices, machine validation reports, and SHA-256 manifests.

## Release boundary

This inventory records the pre-release candidate surface. It does not create a version tag or GitHub release.
"""
        INVENTORY.write_text(inventory, encoding="utf-8", newline="\n")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        HASHES.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        for relative in HASH_TARGETS:
            path = ROOT / relative
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {relative}")
        HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result

if __name__ == "__main__":
    raise SystemExit(0 if validate(write_outputs=True)["passed"] else 1)
