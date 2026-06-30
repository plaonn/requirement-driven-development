# PR as a Development Loop

In RDD, a pull request is not just a bundle of code changes. It is a small development loop with a traceable purpose:

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

## One stable purpose

A PR should have one stable requirement or purpose. That purpose can be a feature, bug fix, refactoring, migration, documentation change, or operational improvement.

The important point is not that the PR is tiny. The important point is that reviewers can tell what requirement defines the loop boundary.

## PR traceability

A good PR description should expose the path from intent to code:

```text
Requirement:
  What need does this PR satisfy?

Spec:
  What rules, contracts, boundaries, or acceptance criteria express the requirement?

Tests:
  What checks protect those rules?

Implementation:
  What changed to satisfy the tests and requirement?

Non-goals:
  What is intentionally out of scope?

Requirement changes discovered:
  Did implementation or review show that the original requirement needs to change?
```

## Recommended PR structure

Use this structure when a PR is large enough that reviewers need explicit context:

```text
# Requirement

# Spec

# Tests

# Implementation

# Non-goals

# Requirement changes discovered

# Review focus
```

The goal is not ceremony. The goal is to make scope and traceability reviewable.

## Scope creep detection

Scope creep often appears as useful-looking work that is not connected to the requirement.

Reviewers should watch for:

- unrelated behavior changes,
- refactoring that changes behavior without saying so,
- bug fixes discovered during implementation but folded into the same PR,
- tests that protect behavior outside the stated requirement,
- expanded API behavior not mentioned in the spec,
- documentation claims broader than the implemented change.

When this happens, the team should decide whether the PR requirement changed or whether the extra work should move to a follow-up loop.

## Split, re-scope, or follow up

When the work no longer fits the original requirement, choose one of these paths:

- **Split** when unrelated requirements can be reviewed independently.
- **Re-scope** when the original requirement was incomplete and the current PR should explicitly own the new boundary.
- **Create a follow-up** when the discovery is valid but not needed to satisfy the current requirement.

RDD does not require every discovery to become a new PR. It requires the boundary decision to be explicit.

## Reviewer responsibility

Reviewers should check code quality, but they should also check requirement traceability:

- Is the driving requirement clear?
- Does the spec express that requirement?
- Do the tests protect meaningful rules?
- Does the implementation satisfy the requirement without hidden scope growth?
- Did the requirement change during implementation?

A technically clean PR can still be a poor RDD loop if it solves a different problem than the one it started with.
