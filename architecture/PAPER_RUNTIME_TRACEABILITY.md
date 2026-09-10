# AOMS Paper-Runtime Traceability

| Foundational proposition | Paper status | v1 evidence | Phase II requirement |
|---|---|---|---|
| Authorization does not imply execution permission | Canonical | Demonstrated by 100 decline cases | Preserve and test directly |
| Authority conditions must be reconstructed | Canonical | Approximated by current-state comparison | Implement explicit reconstruction |
| Execution must fail closed | Canonical | Binary decline on detected violations | Prove compositionally |
| Required stages cannot be bypassed | Canonical | Not structurally enforced as six engines | Enforce ordered orchestration |
| Downstream objects cannot replace upstream objects | Canonical | Objects not separately represented | Enforce typed interfaces |
| Decisions must be condition-sensitive | Canonical | Demonstrated through altered current state | Add paired-trajectory tests |
| `ALLOW` requires positive eligibility | Canonical | Simplified Boolean implementation | Implement EligibilityRecord |
| Unknown critical state cannot produce `ALLOW` | Canonical | Partial | Add explicit unknown-state semantics |
| Permission cannot be cached across execution points | Canonical | Not tested | Add non-cacheability tests |
| `ALLOW` carries complete provenance | Canonical | Not completely represented | Add integrity-linked provenance chain |
