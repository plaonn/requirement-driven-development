# RDD Coding Prompt Template

Work on this task as a requirement-driven loop.

## Need / goal context

State the stakeholder problem, desire, or desired outcome that justifies this task, including the source when known.

## Requirement

State the stable capability, quality, constraint, or condition this task must satisfy. Do not use a goal or desired outcome alone as the loop requirement.

Include:

- Root goal, when this task is part of a larger product or operational direction.
- Decision class, when the loop records a policy, workaround, implementation choice, or promotion candidate instead of a durable requirement.
- Rationale: why this requirement matters.
- Failure prevented: what risk, regression, or bad outcome this requirement prevents.
- Assumptions and revisit conditions for durable requirements.
- Acceptance scope, policy horizon, promotion rule, and expiration rule for temporary policies or scoped risk decisions.

For automation or state-changing work, also state:

- Automate now.
- Require human review.
- Do not automate yet.

## Spec

List the rules, contracts, boundaries, and acceptance criteria that express the requirement.

## Tests / Checks

List the tests or checks that should protect the spec.

## Non-goals

List adjacent work that must stay out of scope.

## Instructions

- Keep the requirement stable for this loop.
- Keep the need or goal as justification context; use the requirement to state what must be true.
- If the root goal, rationale, failure prevented, or automation boundary is unclear, ask boundary clarification questions before producing a full trace.
- Do not treat implementation choices, provider workarounds, or temporary experiment policies as durable requirements unless their rationale and promotion rule are explicit.
- If a decision is marked accepted, state whether it is system-wide, beta-only, operator-run-specific, or blocked from implementation.
- If a long-term goal and the current safety stage appear to conflict, express them as staged requirements.
- Refine specs and tests only when they still express the same requirement.
- If the requirement appears to change, stop and report before expanding scope.
- Preserve the non-goals.
- Do not add adjacent behavior just because it is convenient during implementation.
- Summarize the final trace:

```text
Requirement -> Spec -> Tests/Checks -> Implementation
```
