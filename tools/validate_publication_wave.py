import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = [
    "publications/AOMS-002_MATHEMATICAL_FOUNDATIONS.md",
    "publications/AOMS-003_VERIFICATION_METHODOLOGY.md",
    "publications/AOMS-004_EXECUTION_GOVERNANCE_STACK.md",
    "specifications/AOMS-SPEC-003_STATE_AND_TRANSITION_ALGEBRA.md",
    "specifications/AOMS-SPEC-004_EVIDENCE_AND_PROVENANCE.md",
    "crosswalks/PUBLICATION_RUNTIME_CROSSWALK.csv",
    "registries/AOMS-RG-023_PUBLICATION_CLAIM_REGISTRY.csv",
    "architecture/PHASE_II_PUBLICATION_MANIFEST.md",
]


def validate():
    errors = []
    for rel in EXPECTED:
        path = ROOT / rel
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing_or_empty:{rel}")

    required_sections = {
        "publications/AOMS-002_MATHEMATICAL_FOUNDATIONS.md": ["## Abstract", "## 2. Reconstruction operator", "## 7. Proof obligations"],
        "publications/AOMS-003_VERIFICATION_METHODOLOGY.md": ["## Abstract", "## 2. Verification layers", "## 4. Admission rule"],
        "publications/AOMS-004_EXECUTION_GOVERNANCE_STACK.md": ["## Abstract", "## 2. Layer separation", "## 5. Composition rule"],
        "specifications/AOMS-SPEC-003_STATE_AND_TRANSITION_ALGEBRA.md": ["## 4. Transition sequence", "## 5. Decision algebra", "## 6. Invariants"],
        "specifications/AOMS-SPEC-004_EVIDENCE_AND_PROVENANCE.md": ["## 3. Required terminal record", "## 5. Unknown and conflicting evidence", "## 7. Replay resistance"],
    }
    for rel, markers in required_sections.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"missing_section:{rel}:{marker}")

    crosswalk_count = 0
    crosswalk_path = ROOT / "crosswalks/PUBLICATION_RUNTIME_CROSSWALK.csv"
    if crosswalk_path.is_file():
        with crosswalk_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        crosswalk_count = len(rows)
        for row in rows:
            for field in ("runtime_artifact", "verification_artifact"):
                if not (ROOT / row[field]).exists():
                    errors.append(f"unresolved_crosswalk:{row['publication_id']}:{row[field]}")

    claim_count = 0
    claim_path = ROOT / "registries/AOMS-RG-023_PUBLICATION_CLAIM_REGISTRY.csv"
    if claim_path.is_file():
        with claim_path.open(encoding="utf-8", newline="") as handle:
            claims = list(csv.DictReader(handle))
        claim_count = len(claims)
        ids = [row["claim_id"] for row in claims]
        if len(ids) != len(set(ids)):
            errors.append("duplicate_claim_id")
        for row in claims:
            if not (ROOT / row["artifact"]).exists():
                errors.append(f"unresolved_claim:{row['claim_id']}:{row['artifact']}")

    report = {
        "profile": "AOMS-PUB-001",
        "expected_artifacts": len(EXPECTED),
        "crosswalk_entries": crosswalk_count,
        "registered_claims": claim_count,
        "errors": errors,
        "passed": not errors,
    }
    output = ROOT / "reports/publications/BATCH_05_PUBLICATION_VALIDATION.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(validate())
