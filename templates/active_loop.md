# Active RDD Loop Template

Requirement reference: REQ-FIRST-CAPABILITY
Loop unit: one pull request, task, ticket, or local change set
Adoption trigger: none, or the risk-sensitive condition that opened the gate

## Requirement

State the stable requirement boundary for this loop.

## Spec

State the rules, contracts, boundaries, and acceptance criteria derived for this loop.

## Tests / Checks

List the executable tests, builds, reviews, or manual checks that protect the spec. Record the direct acceptance evidence that can classify the requirement as satisfied, unsatisfied, or unknown; unknown is not satisfied.

## Implementation

Record the minimal implementation that satisfies the requirement and spec.

## Review

Check the trace in both directions: `Requirement -> Spec / acceptance -> Implementation / evidence` and `Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome`. Do not treat implementation progress, a commit, or task completion as requirement satisfaction without direct evidence. Record any boundary decision.

For a risk-sensitive adoption loop, also record:

- Requirement coverage:
- Derived behavior spec:
- Decision record needed: yes | no
- Validation evidence:

## Non-goals

List adjacent work that remains outside this loop.
