# RDD Tooling

This directory contains small read-only helpers for Requirement Driven Development.

The tooling is retrieval and compression support. It is not the source of truth.
Canonical RDD truth remains in the project documents, pull request descriptions,
task notes, tests, and implementation.

## Commands

```sh
python3 tools/rdd/rdd.py trace <path>
python3 tools/rdd/rdd.py trace <path> --json
python3 tools/rdd/rdd.py prompt <path>
python3 tools/rdd/rdd.py prompt <path> --json
python3 tools/rdd/rdd.py gaps <path>
python3 tools/rdd/rdd.py gaps <path> --json
python3 tools/rdd/rdd.py validate <requirements-source> [<requirements-source> ...]
python3 tools/rdd/rdd.py validate <requirements-source> --loops <active-loop-directory>
python3 tools/rdd/rdd.py ready <requirements-source> --loops <active-loop-directory>
```

`<path>` may be a Markdown file or a directory. Directory scans read `.md` files
recursively. `.private/` is skipped unless it is passed explicitly.

## Scope

The first slice intentionally stays narrow:

- Python standard library only.
- No package manager, lockfile, or build step.
- No writes to source documents.
- No generated requirement ledger.
- No task or PR creation.
- No inference of missing rationale.

## Extraction Model

The parser recognizes ATX Markdown headings such as `# Requirement` and
`## Tests`. Headings inside fenced code blocks are ignored.

The parser also recognizes inline field labels in bullet or plain-line form:

```md
- Requirement: ...
- Rationale: ...

요구사항: ...
근거: ...
방지 실패: ...
```

The parser also recognizes compact RDD hierarchy blocks. Numeric headings may
use either `R0: Title` or `R0. Title`; use one style consistently within a
document.

```md
### R0: Root goal title

- Requirement: ...
- Rationale: ...
- Failure prevented: ...
- Assumptions: ...
- Revisit when: ...
```

`R0` is treated as a root goal candidate. `R1`, `R2`, and later blocks are
treated as requirement entries when they contain recognized bullet fields.

The same extractor recognizes an optional semantic hierarchy:

```md
## ROOT-REQ-TRACEABLE-LOOPS: Keep loops traceable

- Parent: none
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: Development loops remain traceable through review.
- Rationale: Reviewers need stable intent while implementation changes.
- Failure prevented: Passing checks can otherwise hide requirement drift.
- Assumptions: Small reviewable development loops remain useful.
- Derived specs: Reviews check the trace from requirement through implementation.
- Revisit when: The project adopts another traceability boundary.

## REQ-READ-ONLY-ANALYSIS: Keep analysis read-only

- Parent: ROOT-REQ-TRACEABLE-LOOPS
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: Analysis must not cause external state changes.
- Rationale: Read-only analysis must be safe to repeat.
- Failure prevented: An analysis command causes an unintended mutation.
- Assumptions: Analysis and mutation remain separate operations.
- Derived specs: Analysis commands do not call mutation paths.
- Revisit when: The operating model intentionally combines those operations.
```

`ROOT-REQ-*` and `REQ-*` are stable references, not replacements for the RDD
vocabulary. A `Root goal` remains separate justification context. Numeric
hierarchies remain valid and require no migration. An explicit migration may
record old identifiers with `Previous identifiers: R1`. Previous identifiers
remain historical mappings and reserved names; current parents and active loops
must use primary identifiers. The tool never rewrites the source document.

Recognized RDD fields include:

- Root goal
- Need / goal context
- Requirement
- Requirement validity / validity scope
- Rationale
- Failure prevented
- Assumptions
- Revisit when
- Revisit signal status
- Spec
- Tests / Checks
- Implementation
- Non-goals
- Automation boundary
- Decision class
- Durability
- Acceptance scope
- Policy horizon
- Promotion rule
- Expiration rule
- Canonical owner
- Boundary clarification
- Review focus
- Requirement changes discovered
- Revalidation outcome
- Affected traces

English and Korean companion labels are supported for common RDD fields. The
alias set also covers retroactive review outputs such as recovered requirements,
derived specs, retroactive coverage, automation boundary decisions, and scoped
policy or decision records.

Missing required fields are reported as boundary clarification questions. The
automation boundary is reported as a conditional gap because it is required only
for automation or state-changing work.

Validity scope is part of the core trace. When a trace declares a durable
requirement, `gaps` also requires assumptions and observable `Revisit when`
signals. When it declares a temporary or scoped policy, `gaps` requires an
expiration rule. Revalidation outcomes and affected traces are extracted when
present but are only needed after a revisit signal occurs.

When a directory scan finds current-truth surfaces such as README, SPEC,
ROADMAP, docs, or test documentation but the core requirement trace is
incomplete, `gaps` also recommends starting with a read-only retroactive RDD
coverage review before promoting recovered candidates into source-of-truth docs
or implementation work.

## JSON

JSON output uses schema version `rdd.trace.v1`.

The JSON shape is intended for agent and tool integration, while Markdown output
is intended for human review.

Semantic extraction uses the same `rdd.trace.v1` shape. Requirement identifiers,
parents, and migration aliases are kept in the structural validator's internal
model rather than added to the existing trace schema.

## Structural validation

`validate` checks one or more explicitly designated requirement files or
directories as one source set. Directory sources are scanned recursively for
Markdown, excluding `README.md` and dotfiles. This supports a compact index plus
split requirement detail documents while still enforcing uniqueness across the
set. It accepts a numeric hierarchy or a semantic hierarchy, but reports mixed
primary representations in one source-of-truth hierarchy.

Semantic validation checks:

- exactly one `ROOT-REQ-*` entry,
- `Parent: none` and `Decision class: Durable Requirement` on the root,
- unique primary and previous identifiers,
- required durable fields,
- defined parents and an acyclic hierarchy.

Active-loop validation checks:

- an optional project-configured filename pattern,
- `Requirement reference` and `Loop unit` metadata,
- a reference to a defined primary requirement identifier,
- `Spec`, `Tests` or `Checks`, `Implementation`, `Review`, and `Non-goals`
  headings.

The headings may be placeholders while work is active. Validation does not
interpret their content, checkbox state, exit conditions, semantic correctness,
or whether current truth has been promoted.

Without `--loops`, `validate` checks only the requirement source set. With an
active-loop directory, `README.md`, dotfiles, and paths passed through repeatable
`--exclude-loop` options are support files rather than active loops. Loop naming
is a project policy; enforce one only when `--loop-name-pattern` is supplied.
For example, lowercase kebab names can be required with
`--loop-name-pattern '^[a-z0-9]+(?:-[a-z0-9]+)*\.md$'`.

`validate` permits structurally valid active-loop documents. `ready` requires
`--loops`, performs the same validation, and then fails if any active-loop
document remains. This makes `ready` an opt-in check for a project that chose the
disposable active-loop pattern; it is not an RDD-wide archive policy.

Example active loop:

```md
# Add semantic requirement parsing

Requirement reference: REQ-SEMANTIC-PARSING
Loop unit: one pull request

## Spec

## Tests / Checks

## Implementation

## Review

## Non-goals
```

Exit codes:

- `0`: valid or ready,
- `1`: structural or lifecycle contract violation,
- `2`: invalid invocation, I/O failure, or unexpected guard execution failure.

Existing `trace`, `prompt`, and `gaps` command behavior and the
`rdd.trace.v1` schema remain backward compatible.

## Test

```sh
python3 tools/rdd/test_rdd.py
```
