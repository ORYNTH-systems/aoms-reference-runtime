# AOMS Phase II Canonical Case Suite

This directory contains exactly 250 machine-readable proofs, `AOMS-101` through `AOMS-350`. The original 100 v1 adversarial cases remain unchanged in the parent directory.

| Decision | Cases | Function |
|---|---:|---|
| `ALLOW` | 25 | Positive controls proving fully continuous authorized execution |
| `REAUTHORIZE` | 75 | Authority, time, actor, action, identity, and policy discontinuities |
| `DENY` | 75 | Dependency, resource, environment, evidence, and non-escalatory boundary failures |
| `ESCALATE` | 75 | Personal, psychological, therapeutic, safety, unknown, and compound boundaries |

Run `python src/canonical_cases.py --all` from the repository root. Each case binds source objects, expected terminal decision, and required reason evidence. Boundary labels are governance signals and must not be interpreted as diagnoses.
