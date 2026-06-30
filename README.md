# RDD: Requirement Driven Development

**Requirement Driven Development (RDD)** is a lightweight development methodology for keeping each development loop anchored to a stable requirement and traceable from intent to implementation.

It treats a pull request, task, ticket, or small agile iteration as a closed loop:

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

TDD makes tests the immediate feedback mechanism. SDD makes specs the explicit contract. RDD puts the requirement above both: specs and tests may evolve as understanding improves, but the requirement that defines the loop should remain stable. If the requirement changes, the loop should be explicitly re-scoped.

## Core idea

Every development loop should answer five questions:

1. **Requirement** - What user, product, business, or technical need drives this change?
2. **Spec** - What rules, boundaries, contracts, and acceptance criteria express that requirement?
3. **Test** - What executable checks prove the spec remains satisfied?
4. **Implementation** - What code or document changes satisfy the tests and the original requirement?
5. **Review** - Does the final change remain traceable back to the requirement without hidden scope creep?

RDD is not a replacement for TDD or SDD. It treats them as nested feedback loops.

```text
RDD: Is the development loop still solving the right requirement?
SDD: Is the requirement expressed as a coherent spec?
TDD: Is the spec protected by executable tests?
```

## Why this exists

Small development units often fail in predictable ways:

- A PR starts with one purpose and ends with another.
- Tests pass, but the original requirement is not satisfied.
- A refactoring PR silently changes behavior.
- A bug-fix PR becomes an unreviewed rule change.
- Acceptance criteria are missing, vague, or narrower than the requirement.
- Review focuses on implementation details while losing requirement traceability.

RDD gives teams a simple way to detect these failures early.

## The RDD loop

```text
1. Fix the requirement for the current loop.
2. Derive the spec from the requirement.
3. Derive tests from the spec.
4. Implement only what the loop requires.
5. Review the full trace from requirement to implementation.
6. If the requirement changes, re-scope the loop explicitly.
```

The key distinction:

```text
Spec/test refinement inside the loop is normal.
Requirement change means the loop boundary changed.
```

## PR-scale RDD

RDD is especially useful at pull request scale.

A PR should not be treated as just a bundle of code changes. It should be treated as a small requirement-driven loop.

A good PR should make these relationships visible:

```text
Requirement:
  The reason this PR exists.

Spec:
  The concrete rules and behavior this PR must satisfy.

Tests:
  The checks that protect those rules.

Implementation:
  The minimal change that satisfies the tests and requirement.

Non-goals:
  The changes intentionally kept outside this PR.
```

## When the requirement changes

During implementation or review, the team may discover that the original requirement was wrong or incomplete.

That is not just a test update. It is a loop boundary event.

Possible responses:

- Re-scope the PR and explicitly update the requirement.
- Keep the current PR minimal and open a follow-up.
- Split unrelated discoveries into separate loops.

## Repository structure

```text
docs/
  01-methodology.md
  02-rdd-sdd-tdd-loop.md
  03-pr-as-development-loop.md
  04-review-method.md
  05-examples.md
  06-ai-agent-usage.md

templates/
  pull_request_template.md
  codex_prompt_template.md

examples/
  order-cancel-example.md
  refactoring-example.md
```

## License

This repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
