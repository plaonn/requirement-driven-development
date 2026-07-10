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

The parser also recognizes compact RDD hierarchy blocks:

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

## Test

```sh
python3 tools/rdd/test_rdd.py
```
