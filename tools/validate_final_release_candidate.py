import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/release/BATCH_10_FINAL_RELEASE_AUDIT.json"
MANIFEST = ROOT / "release/AOMS_PHASE_II_FINAL_RELEASE_MANIFEST.md"
HASHES = ROOT / "release/SHA256SUMS_BATCH_10.txt"
VERSION = "2.0.0-rc.1"

HASH_TARGETS = [
    "VERSION", "README.md", "CHANGELOG.md", "release/AOMS_PHASE_II_EVIDENCE_INDEX.md",
    "release/AOMS_PHASE_II_V2_RELEASE_NOTES.md",
    "release/AOMS_PHASE_II_RELEASE_AUTHORIZATION_GATE.md",
    "release/AOMS_PHASE_II_CITATION_READINESS.md",
    "release/AOMS_PHASE_II_LICENSE_POSITION.md",
    "release/AOMS_PHASE_II_FINAL_RELEASE_MANIFEST.md",
    "tools/validate_final_release_candidate.py",
    "tests/test_final_release_candidate.py",
    "reports/release/BATCH_10_FINAL_RELEASE_AUDIT.json",
]

def count(pattern):
    return len(list(ROOT.glob(pattern)))

def validate(write_outputs=True):
    counts = {
        "v1_cases": count("cases/AOMS-*.json"),
        "canonical_cases": count("cases/canonical/AOMS-*.json"),
        "domain_cases": count("cases/domains/AOMS-B06-*.json"),
        "publication_manuscripts": count("publications/AOMS-*.md"),
        "normative_specifications": count("specifications/AOMS-SPEC-*.md"),
        "registry_artifacts": count("registries/AOMS-RG-*"),
    }
    counts["total_cases"] = counts["v1_cases"] + counts["canonical_cases"] + counts["domain_cases"]
    with (ROOT / "crosswalks/AOMS_CLAIM_TO_PROOF_MATRIX.csv").open(encoding="utf-8", newline="") as handle:
        claims = list(csv.DictReader(handle))
    prior = json.loads((ROOT / "reports/release/BATCH_09_PRERELEASE_AUDIT.json").read_text(encoding="utf-8"))
    required = [
        "CITATION.cff", "release/AOMS_PHASE_II_LICENSE_POSITION.md", "manuals/REPRODUCIBILITY.md",
        "release/AOMS_PHASE_II_RELEASE_CANDIDATE_MANIFEST.md",
        "release/AOMS_PHASE_II_RELEASE_AUTHORIZATION_GATE.md",
        "release/AOMS_PHASE_II_CITATION_READINESS.md",
    "release/AOMS_PHASE_II_LICENSE_POSITION.md",
    ]
    checks = {
        "candidate_version_exact": (ROOT / "VERSION").read_text(encoding="utf-8").strip() == VERSION,
        "v1_case_count_100": counts["v1_cases"] == 100,
        "canonical_case_count_250": counts["canonical_cases"] == 250,
        "domain_case_count_60": counts["domain_cases"] == 60,
        "total_case_count_410": counts["total_cases"] == 410,
        "closed_claim_count_20": len(claims) == 20,
        "all_claims_execution_verified": all(row.get("proof_status") == "EXECUTION-VERIFIED" for row in claims),
        "batch_09_audit_passed": prior.get("passed") is True,
        "required_release_surfaces_present": all((ROOT / item).is_file() for item in required),
        "no_release_action_declared": prior.get("release_action_performed") is False,
    }
    result = {
        "profile": "AOMS-RELEASE-CANDIDATE-001",
        "version": VERSION,
        "counts": counts,
        "closed_claims": len(claims),
        "checks": checks,
        "errors": sorted(name for name, passed in checks.items() if not passed),
        "passed": all(checks.values()),
        "tag_created": False,
        "github_release_created": False,
        "doi_assigned": False,
        "release_authorized": False,
    }
    if write_outputs:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        text = f"""# AOMS Phase II Final Release-Candidate Manifest

## Identity

- Candidate version: `{VERSION}`
- Audit profile: `AOMS-RELEASE-CANDIDATE-001`
- Release authorized: no
- Tag created: no
- GitHub release created: no
- DOI assigned by this batch: no
- License granted by this batch: no

## Verified quantitative position

| Surface | Count |
|---|---:|
| Preserved v1 cases | {counts['v1_cases']} |
| Canonical Phase II cases | {counts['canonical_cases']} |
| Executable domain cases | {counts['domain_cases']} |
| Total cases | {counts['total_cases']} |
| Closed publication claims | {len(claims)} |
| Publication manuscripts | {counts['publication_manuscripts']} |
| Normative specifications | {counts['normative_specifications']} |
| Registry artifacts | {counts['registry_artifacts']} |

## Admission condition

The candidate is technically admissible only when every machine check passes and the complete regression suite succeeds. Public release remains blocked by `AOMS_PHASE_II_RELEASE_AUTHORIZATION_GATE.md`.
"""
        MANIFEST.write_text(text, encoding="utf-8", newline="\n")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        lines = []
        for relative in HASH_TARGETS:
            path = ROOT / relative
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}")
        HASHES.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result

if __name__ == "__main__":
    raise SystemExit(0 if validate(write_outputs=True)["passed"] else 1)
