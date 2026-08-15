# RDD Coding Prompt Template

Work on this task as a requirement-driven loop.

## Need / goal context

State the stakeholder problem, desire, or desired outcome that justifies this task, including the source when known.

## Requirement

State the stable, normative, discriminating, solution-independent capability, quality, constraint, or condition this task must satisfy. Do not use a goal or desired outcome alone as the loop requirement. The requirement should remain stable while internal architecture, APIs, data structures, spec details, or test strategy change; `unknown` evidence is not satisfaction.

Include:

- Requirement identifier, when the project uses a numeric or semantic hierarchy. Preserve the project's chosen representation; do not silently rename or migrate identifiers.
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

For a substantial public capability, OAuth scope, state-changing adapter,
irreversible external effect, financial or live execution path, or
cross-repository ownership, authority, or trust boundary, apply the
risk-sensitive adoption gate:

- Load the relevant requirement source before implementation.
- Name the specific requirement that covers the capability and failure boundary.
- Do not rely only on permission from a broad root goal.
- Decide whether a long-lived decision record is needed.

## Requirement validity

Classify the item as a loop-local requirement, durable requirement, or temporary/scoped policy.

- Validity scope: loop-local requirement, durable requirement, or temporary/scoped policy.
- Assumptions: conditions that must remain true for a durable requirement.
- Revisit when: observable signals that trigger revalidation of a durable requirement.
- Expiration rule: the event or condition that ends a temporary or scoped policy.
- If a revisit signal has occurred, stop deriving new work until the requirement is revalidated as `retain`, `narrow`, `supersede`, or `discard` and affected downstream traces are identified.

## Spec

List the rules, contracts, boundaries, and acceptance criteria that express the requirement.

## Tests / Checks

List the tests or checks that should protect the spec.

## Acceptance evidence / Done when

State the observable evidence that can distinguish whether the requirement is satisfied, unsatisfied, or unknown. `Done when` is a useful downstream label, not a mandatory RDD field.

## Non-goals

List adjacent work that must stay out of scope.

## Instructions

- Keep the requirement stable for this loop.
- Keep the need or goal as justification context; use the requirement to state what must be true.
- Do not treat implementation progress, passing tests that do not cover the requirement, a commit, or task completion as direct requirement evidence.
- Do not treat loop stability as permanent validity. Apply the requirement-validity rules before continuing when a revisit signal occurs.
- If the root goal, rationale, failure prevented, or automation boundary is unclear, ask boundary clarification questions before producing a full trace.
- Do not treat implementation choices, provider workarounds, or temporary experiment policies as durable requirements unless their rationale and promotion rule are explicit.
- If a decision is marked accepted, state whether it is system-wide, beta-only, operator-run-specific, or blocked from implementation.
- If a long-term goal and the current safety stage appear to conflict, express them as staged requirements.
- Refine specs and tests only when they still express the same requirement.
- Internal architecture, internal APIs or data structures, test strategy or location, acceptance refinement for the same requirement, and bounded refactoring are normal refinements. A material change to capability, actor/scope, trigger, obligation, accepted failure mode, user-facing behavior, authority, security/privacy boundary, or public contract requires re-scoping.
- If the requirement appears to change, stop and report before expanding scope.
- Preserve the non-goals.
- Do not add adjacent behavior just because it is convenient during implementation.
- Follow the repository's loop-record retention policy. Do not create an archive or delete an active-loop record unless that policy and the current task authorize it.
- For a risk-sensitive adoption loop, do not report completion until requirement coverage, derived behavior spec, tests/checks, implementation, decision-record disposition, and validation evidence are visible.
- Summarize the final trace:

```text
Requirement -> Spec / acceptance -> Tests/Checks -> Implementation / evidence

Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```
