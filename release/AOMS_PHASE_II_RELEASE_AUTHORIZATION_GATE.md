# AOMS Phase II Release Authorization Gate

## Current state

Candidate `2.0.0-rc.1` is technically prepared but not released.

## Required authorization

No automation in Batch 10 may create or push a Git tag, create a GitHub release, publish an archival deposit, assign or update a DOI, or overwrite a prior release artifact. Those actions require a separate explicit authorization after review of the final commit, audit report, source-archive hash, citation metadata, and release notes.

## Final gate checklist

- Confirm remote master and candidate-branch identities.
- Review the complete staged and committed file boundary.
- Confirm all regression tests and release audits pass.
- Verify the source archive against its independent SHA-256 sidecar.
- Review `CITATION.cff` and planned archival metadata.
- Choose the final semantic version and tag.
- Explicitly authorize or decline public release.
