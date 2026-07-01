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
- Requirement
- Rationale
- Failure prevented
- Assumptions
- Revisit when
- Spec
- Tests / Checks
- Implementation
- Non-goals
- Automation boundary
- Boundary clarification
- Review focus
- Requirement changes discovered

Missing required fields are reported as boundary clarification questions. The
automation boundary is reported as a conditional gap because it is required only
for automation or state-changing work.

## JSON

JSON output uses schema version `rdd.trace.v1`.

The JSON shape is intended for agent and tool integration, while Markdown output
is intended for human review.

## Test

```sh
python3 tools/rdd/test_rdd.py
```
