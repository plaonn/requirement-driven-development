# RDD: Requirement Driven Development

한국어: [README.ko.md](README.ko.md)

**Requirement Driven Development (RDD)** is a lightweight development methodology for keeping each development loop anchored to a stable requirement and traceable from intent through implementation to observable evidence.

It treats a pull request, task, ticket, or small agile iteration as a closed loop:

```text
Need / Goal -> Requirement -> Spec -> Implementation -> Test / Acceptance Evidence -> Review
```

This is a semantic trace, not a required execution order. Tests may be designed before implementation, and evidence may include tests, manual checks, document review, or other observations that directly bear on the requirement.

TDD makes tests the immediate feedback mechanism. SDD makes specs the explicit contract. RDD puts the requirement above both: specs and tests may evolve as understanding improves, but the requirement that defines the loop should remain stable. If the requirement changes, the loop should be explicitly re-scoped.

## Purpose

RDD exists for two things. First, to keep a loop's original direction when context fades, by holding the requirement as an anchor outside anyone's memory. Second, to guarantee autonomy for changes that stay inside the requirement, so only boundary events need a decision. Delegating work to AI agents is the strongest case for both, but the same context loss and delegation problems affect human developers. This is a personal methodology published as-is; use it if you share the purpose.

## Root goal

RDD helps teams keep small development loops aligned with the need and goal that justify them and with the requirement that anchors them, so specs, implementation, acceptance evidence, and review remain traceable and scope changes are made explicit.

## Relationship to requirements engineering

RDD is not a replacement for requirements engineering. Requirements engineering covers the broader work of eliciting, analyzing, negotiating, specifying, validating, and managing requirements across a system or product lifecycle.

RDD operates at a narrower boundary. It assumes that a candidate requirement has been derived from a relevant need or goal and sufficiently elicited and validated for the current development loop, then helps the team keep that requirement traceable through spec, implementation, acceptance evidence, and review. It does not replace stakeholder discovery, product discovery, requirement prioritization, conflict resolution, or system-wide requirements management.

See [RDD and Requirements Engineering](docs/08-rdd-and-requirements-engineering.md) for the detailed boundary.

## Vocabulary boundary

RDD uses a pragmatic vocabulary for keeping the layers of a small loop reviewable:

```text
Need: a stakeholder problem, desire, or expected outcome.
Goal: a desired state that gives direction to one or more requirements.
Requirement: a stable, normative, discriminating, solution-independent capability, quality, constraint, or condition that must be satisfied.
Spec: the current precise expression of the requirement as rules, contracts, boundaries, and acceptance criteria.
```

Need and goal explain why and in which direction the work exists. The requirement states what must be true and anchors the loop. The spec makes the current interpretation precise enough to verify. Requirements engineering uses these terms in several broader ways; this is an explicit RDD convention, not a claim of universal terminology.

In RDD, a useful requirement remains stable while internal architecture, internal APIs, data structures, spec wording, and test strategy change. It is normative: the loop is not complete unless the condition is true. It is discriminating: available evidence can meaningfully classify it as `satisfied`, `unsatisfied`, or `unknown`; `unknown` is not `satisfied`. It is solution-independent: filenames, internal APIs, commands, and test locations are normally spec or implementation details unless they are themselves part of the external contract. If one sentence hides several independently testable obligations, split it into a small number of atomic requirements.

## Core idea

Before opening a loop, confirm the need or goal that justifies its candidate requirement. Every development loop should then answer five questions:

1. **Requirement** - What capability, quality, constraint, or condition must be satisfied in this loop?
2. **Spec** - What rules, boundaries, contracts, and acceptance criteria express that requirement?
3. **Implementation** - What code or document changes realize the current spec and requirement?
4. **Test / acceptance evidence** - What observable evidence can distinguish satisfied, unsatisfied, and unknown?
5. **Review** - Can the implementation and evidence be traced back through spec and acceptance to the original requirement and goal without hidden scope creep?

RDD is not a replacement for TDD or SDD. It treats them as nested feedback loops.

## Minimum semantic trace

Artifact and documentation ceremony may scale with the size and abstraction level of the work, but the minimum semantic trace does not disappear:

```text
Outcome / Goal:
  The desired state that gives the loop direction.

Requirement:
  The stable normative condition that must remain true.

Done when / Acceptance:
  The observable evidence that can determine whether the requirement is satisfied.
```

`Outcome`, `Requirement`, and `Done when` are useful downstream field names, not an RDD-mandated schema. A small PR, task, or agent loop does not need a separate `REQUIREMENTS.md`, active-loop file, or heavyweight artifact when a compact requirement-and-evidence trace in its PR, task note, commit message, or final review is enough. Larger or higher-risk work may need the full trace, durable requirement validity fields, decision records, or other documentation that the project uses.

Implementation progress, passing tests, a commit, or a task marked complete are delivery signals. They do not replace the original requirement or count as direct acceptance evidence when they do not bear on whether that requirement is satisfied.

```text
RDD: Is the development loop still solving the right requirement?
SDD: Is the requirement expressed as a coherent spec?
TDD: Is the spec protected by executable tests?
```

## Scaling and limits

RDD scales by consequence, not size: from no trace for obvious local changes, through the minimum trace for ordinary work, to a start and finish gate for risky changes, to durable records for long-lived requirements. The minimum trace, the `unknown` rule, and the boundary-change rule are the core; hierarchy, identifiers, the validity lifecycle, and tooling are optional extensions. It overlaps with acceptance criteria, ATDD/BDD, and Definition of Done, and its outcomes have not been measured. See [When to Use RDD, and Its Limits](docs/09-applicability-and-limits.md).

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
5. Review the trace from requirement through implementation to direct evidence, then reverse-check evidence and implementation back to the requirement and goal.
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

### Risk-sensitive forward adoption

After the first retroactive pass, existing projects do not need heavyweight RDD
ceremony for every change. Use an explicit start and finish gate when a change
adds a substantial public capability, OAuth scope, state-changing adapter,
irreversible external effect, financial or live execution path, or
cross-repository ownership, authority, or trust boundary.

At the start, load the relevant requirement source and confirm that a specific
loop-local or durable requirement covers the new capability and its failure
boundary. Permission from a broad root goal is not sufficient coverage by
itself. At the finish, verify the trace through spec, implementation, direct
acceptance evidence, and any long-lived architectural decision. See the
[existing-project adoption gate](docs/07-retroactive-rdd-review.md#risk-sensitive-forward-adoption-gate).

## PR-scale RDD

RDD is especially useful at pull request scale.

A PR should not be treated as just a bundle of code changes. It should be treated as a small requirement-driven loop.

When a project does not use pull requests, the same model can be applied at task or change-set scale. The review surface may be a task note, commit message body, agent final trace, or another lightweight record, as long as the requirement boundary remains visible.

Projects may retain completed loop records, delete disposable active-loop files after surviving truth has been promoted, or retain only selected high-value records. RDD does not require one retention policy. It requires the loop boundary and direct requirement-to-evidence trace to be reviewable before completion, while durable requirements, current contracts, tests, and important architectural decisions survive in an appropriate current-truth surface.

A good PR should make these relationships visible:

```text
Requirement:
  The reason this PR exists.

Spec:
  The concrete rules and behavior this PR must satisfy.

Tests / acceptance evidence:
  The checks and observations that directly establish whether the requirement is satisfied.

Implementation:
  The minimal change that satisfies the tests and requirement.

Non-goals:
  The changes intentionally kept outside this PR.
```

## Same-requirement refinement and boundary changes

The following are normal refinement inside the same requirement when they preserve the same external contract: changing internal architecture, internal APIs or data structures, test strategy or location, acceptance criteria to verify the requirement more precisely, and bounded refactoring. They may change the spec, tests, or implementation without requiring a new loop boundary.

The loop must be re-scoped when the change materially changes the capability itself, applicable actor or scope, trigger condition, obligation level, accepted failure mode, user-facing behavior, authority, security or privacy boundary, or other public contract. Those changes alter what must be true, not merely how the same requirement is realized or evidenced.

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
  09-applicability-and-limits.md

skills/
  rdd-retroactive-review/
    SKILL.md

templates/
  requirements.md
  active_loop.md
  pull_request_template.md
  codex_prompt_template.md

examples/
  order-cancel-example.md
  refactoring-example.md
```

## Language policy

English is the only canonical language for the methodology, docs, examples, and templates. `README.ko.md` is a short Korean overview that links back to the English documents; it is not a full translation and is not required to track every change. Tooling accepts Korean field labels for projects that write their records in Korean.

The `skills/` directory contains optional agent workflow instructions that apply the public methodology. RDD itself is not agent-specific.

## License

This repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
