# AOMS Agentic State Category Report

## Scope

This report covers AOMS-071 through AOMS-080.

The Agentic State category tests whether execution is declined when the action being attempted differs from the action that was originally authorized.

## Cases

AOMS-071 Agent Action Drift
AOMS-072 Goal Substitution
AOMS-073 Objective Reinterpretation
AOMS-074 Delegated Agent Drift
AOMS-075 Planner Executor Divergence
AOMS-076 Multi-Agent Coordination Drift
AOMS-077 Agent Capability Change
AOMS-078 Autonomous Task Mutation
AOMS-079 Emergent Agent Behavior
AOMS-080 Agent Intent Continuity Failure

## Expected Violation

action_drift_detected

## Architectural Finding

Authorization is bound to the originally authorized action. Agentic reinterpretation, mutation, substitution, or drift invalidates execution admissibility.

## Protected Invariant

Authorization of one action does not authorize a different action.
