import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "crosswalks" / "AOMS_CLAIM_TO_PROOF_MATRIX.csv"
REGISTRY = ROOT / "registries" / "AOMS-RG-026_CLAIM_PROOF_CLOSURE.csv"
REPORT = ROOT / "reports" / "publications" / "BATCH_08_CLAIM_PROOF_VALIDATION.json"
HASHES = ROOT / "release" / "SHA256SUMS_BATCH_08.txt"


def validate(write_outputs=True):
    errors = []
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["claim_id"] for row in rows]
    if len(rows) != 20:
        errors.append("claim_count_not_20")
    if len(ids) != len(set(ids)):
        errors.append("duplicate_claim_id")
    expected_publications = Counter({"AOMS-002": 8, "AOMS-003": 6, "AOMS-004": 6})
    publication_counts = Counter(row["publication_id"] for row in rows)
    if publication_counts != expected_publications:
        errors.append("publication_distribution_invalid")
    for row in rows:
        if row["proof_status"] != "EXECUTION-VERIFIED":
            errors.append("unverified_claim:" + row["claim_id"])
        for field in ("specification", "runtime_artifact", "execution_case", "proof_report"):
            if not (ROOT / row[field]).exists():
                errors.append("unresolved:" + row["claim_id"] + ":" + field + ":" + row[field])
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        closures = list(csv.DictReader(handle))
    if len(closures) != 3:
        errors.append("closure_count_not_3")
    for closure in closures:
        if closure["status"] != "CLOSED":
            errors.append("closure_not_closed:" + closure["closure_id"])
        if not (ROOT / closure["evidence_appendix"]).is_file():
            errors.append("missing_appendix:" + closure["closure_id"])
    aggregate = json.loads((ROOT / "reports/domain-execution/BATCH_07_AGGREGATE.json").read_text(encoding="utf-8"))
    if aggregate.get("status") != "EXECUTION-VERIFIED" or aggregate.get("failed") != 0:
        errors.append("batch_07_execution_not_verified")
    result = {
        "profile": "AOMS-CLOSURE-001",
        "claim_count": len(rows),
        "publication_counts": dict(sorted(publication_counts.items())),
        "closure_count": len(closures),
        "errors": errors,
        "passed": not errors,
    }
    if write_outputs:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        targets = [
            MATRIX, REGISTRY,
            ROOT / "architecture/PHASE_II_CLAIM_PROOF_CLOSURE.md",
            ROOT / "publications/appendices/AOMS-002_EVIDENCE_APPENDIX.md",
            ROOT / "publications/appendices/AOMS-003_EVIDENCE_APPENDIX.md",
            ROOT / "publications/appendices/AOMS-004_EVIDENCE_APPENDIX.md",
            ROOT / "release/AOMS_PHASE_II_RELEASE_CANDIDATE_MANIFEST.md",
            ROOT / "release/AOMS_PHASE_II_EVIDENCE_INDEX.md",
            ROOT / "tools/validate_claim_proof_closure.py",
            ROOT / "tests/test_claim_proof_closure.py",
            REPORT,
        ]
        HASHES.parent.mkdir(parents=True, exist_ok=True)
        with HASHES.open("w", encoding="utf-8", newline="\n") as handle:
            for path in targets:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                handle.write(digest + "  " + path.relative_to(ROOT).as_posix() + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    raise SystemExit(0 if validate(write_outputs=True)["passed"] else 1)
