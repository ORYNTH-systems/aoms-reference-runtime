# AOMS Execution Specification

## Purpose

This specification defines the minimum runtime model for determining whether a previously authorized action remains eligible for execution.

## Core State Objects

### AuthorizedState

Represents the conditions that existed when authorization was granted.

Fields:

- `authorization_id`
- `actor_id`
- `authorized_action`
- `authorized_at`
- `expires_at`
- `authority_valid`
- `policy_version`
- `dependency_state`
- `resource_state`
- `environment_state`

### CurrentState

Represents the conditions that exist when execution is attempted.

Fields:

- `actor_id`
- `current_action`
- `execution_attempted_at`
- `authority_valid`
- `policy_version`
- `dependency_state`
- `resource_state`
- `environment_state`

### ReconciliationResult

Represents the comparison between AuthorizedState and CurrentState.

Fields:

- `reconciliation_required`
- `violations`
- `admissibility`

### ExecutionResult

Represents the final runtime outcome.

Allowed values:

- `APPROVED`
- `DECLINED`

## Admissibility Rules

Execution is admissible only if all of the following are true:

1. authority remains valid,
2. authorization has not expired,
3. current action matches authorized action,
4. policy version remains compatible,
5. dependency state remains valid,
6. resource state remains available,
7. environment state remains valid.

## Violation Codes

- `authority_invalid`
- `authorization_expired`
- `action_drift_detected`
- `policy_changed`
- `dependency_state_changed`
- `resource_unavailable`
- `environment_invalid`

## Execution Flow

1. Load authorized state.
2. Load current execution state.
3. Reconstruct current admissibility.
4. Detect violations.
5. Determine admissibility.
6. Return `APPROVED` or `DECLINED`.

## Protected Invariant

AOMS must never approve execution solely because prior authorization exists.

Execution may be approved only after current-state reconciliation confirms admissibility.
