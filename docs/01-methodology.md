# RDD Methodology

Requirement Driven Development (RDD) is a lightweight methodology for keeping small development loops aligned with their driving requirement.

RDD is based on a simple claim:

```text
A development loop is healthy when its requirement, spec, tests, implementation, and review remain traceable to each other.
```

## Development loop

A development loop may be a pull request, a task, a ticket, a story, a bug fix, or a small agile iteration.

RDD is intentionally scoped to small loops. It does not try to replace product discovery, roadmap planning, Scrum, Kanban, XP, or TDD. It gives those practices a traceability model for day-to-day development work.

## The loop boundary

In RDD, every loop needs a stable requirement.

That requirement defines the boundary of the loop:

```text
Inside the loop:
  Refining specs
  Adding examples
  Adding tests
  Simplifying implementation
  Clarifying acceptance criteria

Outside the loop:
  Changing the underlying requirement
  Expanding the goal to a different user need
  Mixing unrelated fixes
  Adding opportunistic behavior changes
```

A requirement can be wrong. A requirement can be incomplete. A requirement can change after learning.

RDD does not deny that. It only says that when the requirement changes, the loop boundary has changed too. That change should be explicit.

## Roles of each layer

### Requirement

The requirement explains why the work exists.

Good requirements are not always long, but they should be clear enough to distinguish success from unrelated change.

Examples:

```text
Users can cancel an order before fulfillment starts.

The report export should preserve the same filters visible in the UI.

The parser should reject malformed input with actionable errors.

This refactoring should isolate receipt formatting without changing pricing behavior.
```

### Spec

The spec translates the requirement into rules, contracts, boundaries, and acceptance criteria.

Specs may evolve inside the loop as the team learns more about the requirement.

### Test

Tests make parts of the spec executable.

Tests are not the requirement itself. They are a protection mechanism for the current interpretation of the spec.

### Implementation

Implementation satisfies the tests and the original requirement.

Passing tests is necessary but not sufficient if the implementation violates the requirement's intent or expands beyond the loop boundary.

### Review

Review checks the full trace:

```text
Requirement -> Spec -> Test -> Implementation
```

A good review asks not only whether the code works, but whether the work still belongs to the current loop.

## Core rule

```text
Spec and test refinement may happen inside the loop.
Requirement change must be made explicit as a loop boundary change.
```

This is the practical center of RDD.
