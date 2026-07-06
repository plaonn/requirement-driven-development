# RDD: Requirement Driven Development

한국어: [README.ko.md](README.ko.md)

**Requirement Driven Development (RDD)** is a lightweight development methodology for keeping each development loop anchored to a stable requirement and traceable from intent to implementation.

It treats a pull request, task, ticket, or small agile iteration as a closed loop:

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

TDD makes tests the immediate feedback mechanism. SDD makes specs the explicit contract. RDD puts the requirement above both: specs and tests may evolve as understanding improves, but the requirement that defines the loop should remain stable. If the requirement changes, the loop should be explicitly re-scoped.

## Root goal

RDD helps teams keep small development loops aligned with the requirement that justifies them, so specs, tests, implementation, and review remain traceable and scope changes are made explicit.

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

## Existing projects

When applying RDD to an existing project, do not treat existing specs, tests, or
implementation behavior as proof that the project already has confirmed
requirements.

Start with [Retroactive RDD Review](docs/07-retroactive-rdd-review.md). The
first pass should be read-only: recover candidate requirements, identify trace
gaps, and decide what needs confirmation before anything is promoted into
source-of-truth docs.

A `SPEC.md`, roadmap, test suite, or stable implementation can be useful
evidence, but it is not enough by itself. If the root goal, rationale, failure
prevented, or loop boundary is missing or unclear, keep the recovered item as a
candidate and clarify the boundary before implementation or documentation
adoption.

Some confirmed decisions should remain scoped policies rather than durable
requirements. Temporary experiment policies, provider workarounds, and
operator-run-specific risk decisions should carry acceptance scope, promotion
rules, and expiration rules so they do not harden into permanent requirements by
accident.

## PR-scale RDD

RDD is especially useful at pull request scale.

A PR should not be treated as just a bundle of code changes. It should be treated as a small requirement-driven loop.

When a project does not use pull requests, the same model can be applied at task or change-set scale. The review surface may be a task note, commit message body, agent final trace, or another lightweight record, as long as the requirement boundary remains visible.

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
README.md
README.ko.md

docs/
  01-methodology.md
  02-rdd-sdd-tdd-loop.md
  03-pr-as-development-loop.md
  04-review-method.md
  05-examples.md
  06-ai-agent-usage.md
  07-retroactive-rdd-review.md
  ko/
    01-methodology.md
    02-rdd-sdd-tdd-loop.md
    03-pr-as-development-loop.md
    04-review-method.md
    05-examples.md
    06-ai-agent-usage.md
    07-retroactive-rdd-review.md

skills/
  rdd-retroactive-review/
    SKILL.md

templates/
  pull_request_template.md
  codex_prompt_template.md
  pull_request_template.ko.md
  codex_prompt_template.ko.md

examples/
  order-cancel-example.md
  refactoring-example.md
  ko/
    order-cancel-example.md
    refactoring-example.md
```

Korean companion documents are provided for readers who prefer Korean. The English documents remain the canonical public structure.

The `skills/` directory contains optional agent workflow instructions that apply the public methodology. RDD itself is not agent-specific.

## License

This repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
