# RDD: Requirement Driven Development

한국어: [README.ko.md](README.ko.md)

**Requirement Driven Development (RDD)** is a lightweight development methodology for keeping each development loop anchored to a stable requirement and traceable from intent to implementation.

It treats a pull request, task, ticket, or small agile iteration as a closed loop:

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

TDD makes tests the immediate feedback mechanism. SDD makes specs the explicit contract. RDD puts the requirement above both: specs and tests may evolve as understanding improves, but the requirement that defines the loop should remain stable. If the requirement changes, the loop should be explicitly re-scoped.

## Root goal

RDD helps teams keep small development loops aligned with the need and goal that justify them and with the requirement that anchors them, so specs, tests, implementation, and review remain traceable and scope changes are made explicit.

## Relationship to requirements engineering

RDD is not a replacement for requirements engineering. Requirements engineering covers the broader work of eliciting, analyzing, negotiating, specifying, validating, and managing requirements across a system or product lifecycle.

RDD operates at a narrower boundary. It assumes that a candidate requirement has been derived from a relevant need or goal and sufficiently elicited and validated for the current development loop, then helps the team keep that requirement traceable through spec, tests, implementation, and review. It does not replace stakeholder discovery, product discovery, requirement prioritization, conflict resolution, or system-wide requirements management.

See [RDD and Requirements Engineering](docs/08-rdd-and-requirements-engineering.md) for the detailed boundary.

## Vocabulary boundary

RDD uses a pragmatic vocabulary for keeping the layers of a small loop reviewable:

```text
Need: a stakeholder problem, desire, or expected outcome.
Goal: a desired state that gives direction to one or more requirements.
Requirement: a capability, quality, constraint, or condition that must be satisfied.
Spec: the current precise expression of the requirement as rules, contracts, boundaries, and acceptance criteria.
```

Need and goal explain why and in which direction the work exists. The requirement states what must be true and anchors the loop. The spec makes the current interpretation precise enough to verify. Requirements engineering uses these terms in several broader ways; this is an explicit RDD convention, not a claim of universal terminology.

## Core idea

Before opening a loop, confirm the need or goal that justifies its candidate requirement. Every development loop should then answer five questions:

1. **Requirement** - What capability, quality, constraint, or condition must be satisfied in this loop?
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

## Requirement validity lifecycle

RDD should make it possible to recognize when an existing requirement may no longer be valid. It does this by recording validity conditions before the requirement becomes stale, not by assuming that a passing test proves the requirement is still needed.

```text
Validity scope:
  Loop-local requirement | Durable requirement | Temporary/scoped policy

Assumptions:
  Conditions that must remain true for the requirement to stay valid.

Revisit when:
  Observable signals that trigger revalidation.
```

A temporary or scoped constraint should normally remain a policy with an expiration rule rather than be promoted into the durable requirement set. A revisit signal does not automatically invalidate a requirement. It marks a boundary event: revalidate the linked need, goal, rationale, and assumptions, then explicitly `retain`, `narrow`, `supersede`, or `discard` the requirement. Propagate that decision to affected specs, tests, implementation, and active loops.

## Requirement identifiers

RDD does not require one identifier format. Existing numeric hierarchies such as `R0`, `R1`, and `R2` remain valid. Projects that benefit from stable semantic references may instead use one `ROOT-REQ-*` identifier for the root requirement and `REQ-*` identifiers for its descendants. A root goal remains separate justification context rather than becoming a requirement merely because it appears near the hierarchy root.

Semantic identifiers are stable current-truth references. Once adopted, they should not be silently renamed, reused, or renumbered. Migration from numeric identifiers is optional and should preserve an explicit old-to-new mapping rather than rewriting history.

## Adopting RDD structure and tooling

Existing numeric RDD projects can start with hierarchy-only validation and do not need to create an active-loop directory or migrate identifiers. New semantic projects can start from [the requirement hierarchy template](templates/requirements.md). Projects with split requirement details may pass multiple files or directories as one source set.

```sh
python3 tools/rdd/rdd.py validate REQUIREMENTS.md
python3 tools/rdd/rdd.py validate REQUIREMENTS.md docs/requirements/
```

Projects that choose the disposable active-loop pattern can start from [the active-loop template](templates/active_loop.md), add `--loops` during work, and use `ready` as the merge-ready structural check. Persistent or selective-retention projects may omit `ready` or point it only at a dedicated active-work directory.

```sh
python3 tools/rdd/rdd.py validate REQUIREMENTS.md --loops rdd/loops/
python3 tools/rdd/rdd.py ready REQUIREMENTS.md --loops rdd/loops/
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

Projects may retain completed loop records, delete disposable active-loop files after surviving truth has been promoted, or retain only selected high-value records. RDD does not require one retention policy. It requires the loop boundary to be reviewable before completion and durable requirements, current contracts, tests, and important architectural decisions to survive in an appropriate current-truth surface.

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
  08-rdd-and-requirements-engineering.md
  ko/
    01-methodology.md
    02-rdd-sdd-tdd-loop.md
    03-pr-as-development-loop.md
    04-review-method.md
    05-examples.md
    06-ai-agent-usage.md
    07-retroactive-rdd-review.md
    08-rdd-and-requirements-engineering.md

skills/
  rdd-retroactive-review/
    SKILL.md

templates/
  requirements.md
  active_loop.md
  pull_request_template.md
  codex_prompt_template.md
  requirements.ko.md
  active_loop.ko.md
  pull_request_template.ko.md
  codex_prompt_template.ko.md

examples/
  order-cancel-example.md
  refactoring-example.md
  ko/
    order-cancel-example.md
    refactoring-example.md
```

## Companion documentation policy

English documents are the canonical public structure. Korean companions use natural Korean rather than sentence-by-sentence literal translation, while preserving the same reader-facing concepts, rules, non-goals, warnings, examples, and section structure.

When reader-facing meaning changes in an English document, update its Korean companion in the same change. Mark intentional Korean-only explanations with `companion-only` comments. Run `python3 tools/check_companion_docs.py` to detect structural drift, then review semantic equivalence separately. CI runs the structural check on pushes and pull requests.

The `skills/` directory contains optional agent workflow instructions that apply the public methodology. RDD itself is not agent-specific.

## License

This repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
