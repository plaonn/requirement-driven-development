# RDD with AI Coding Agents

AI coding agents are one application area for RDD, not the main purpose of the methodology.

RDD applies to ordinary software work first: pull requests, tickets, tasks, and small iterations. Agents benefit from the same structure because they are especially likely to follow implementation momentum into adjacent work unless the loop boundary is explicit.

## Agent loop boundary

When using an agent, give it a stable requirement, explicit spec, tests, and non-goals.

The agent should be allowed to refine specs and tests only when they still express the same requirement. If the requirement appears to change, the agent should stop and report before expanding scope.

## Useful agent instructions

Give agents instructions in this shape:

```text
Requirement:
  The stable requirement this task must satisfy.

Spec:
  Rules, contracts, acceptance criteria, and boundaries.

Tests:
  Required tests or checks.

Non-goals:
  Adjacent work that must stay out of scope.

Stop conditions:
  Conditions that require reporting back instead of continuing.
```

## Stop conditions

Agents should stop or report when:

- the requirement appears wrong or incomplete,
- implementation suggests an adjacent feature,
- tests need to be changed in a way that alters the requirement,
- a discovered bug belongs to a different requirement,
- non-goals appear necessary to complete the task,
- the requested change requires a broader architecture or API decision.

## Scope discipline

An agent should not expand scope just because implementation suggests adjacent work.

Examples:

- A cancellation task should not become order editing.
- A refactoring task should not hide behavior changes.
- A bug fix should not redesign a related workflow unless explicitly re-scoped.

## Final trace

At the end of the task, the agent should summarize:

```text
Requirement -> Spec -> Tests -> Implementation
```

That final trace helps reviewers decide whether the work stayed inside the loop.
