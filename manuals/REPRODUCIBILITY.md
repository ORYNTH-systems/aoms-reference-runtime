# AOMS Phase II Reproducibility Guide

## Supported verification path

Run commands from the repository root with Python 3. The reference implementation uses only the Python standard library.

```powershell
python tools/validate_publication_wave.py
python tools/validate_domain_benchmarks.py
python tools/validate_claim_proof_closure.py
python tools/validate_prerelease_audit.py
python -m unittest discover -s tests -v
```

## Expected position

- Preserved v1 cases: 100.
- Canonical Phase II cases: 250.
- Executable domain cases: 60.
- Total case corpus: 410.
- Closed publication claims: 20.
- Domain profiles: AI agents, finance, healthcare, robotics, civic systems, and emergency response.
- Terminal decisions: ALLOW, DENY, ESCALATE, and REAUTHORIZE.

## Evidence inspection

The aggregate domain proof is `reports/domain-execution/BATCH_07_AGGREGATE.json`. Claim closure is recorded in `reports/publications/BATCH_08_CLAIM_PROOF_VALIDATION.json`. The Batch 09 audit report is `reports/release/BATCH_09_PRERELEASE_AUDIT.json`. Frozen Batch 09 artifact hashes are in `release/SHA256SUMS_BATCH_09.txt`.

## Boundary

Successful reproduction establishes consistency with this reference repository and its declared fixtures. It does not establish deployment safety, legal compliance, professional authorization, standards adoption, peer review, or third-party certification.
