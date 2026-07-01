# RDD Coding Prompt Template

Work on this task as a requirement-driven loop.

## Requirement

State the stable requirement this task must satisfy.

Include:

- Root goal, when this task is part of a larger product or operational direction.
- Rationale: why this requirement matters.
- Failure prevented: what risk, regression, or bad outcome this requirement prevents.
- Assumptions and revisit conditions for durable requirements.

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
- Do not treat implementation choices as requirements unless their rationale is explicit.
- If a long-term goal and the current safety stage appear to conflict, express them as staged requirements.
- Refine specs and tests only when they still express the same requirement.
- If the requirement appears to change, stop and report before expanding scope.
- Preserve the non-goals.
- Do not add adjacent behavior just because it is convenient during implementation.
- Summarize the final trace:

```text
Requirement -> Spec -> Tests/Checks -> Implementation
```
