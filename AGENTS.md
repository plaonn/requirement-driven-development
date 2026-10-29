# Project Instructions

## Project Purpose

This repository documents Requirement Driven Development (RDD), a lightweight methodology for keeping small development loops traceable from requirement to spec, tests, implementation, and review.

Preserve the repository's public role as a methodology/documentation project. Do not turn it into a project-management tool or framework unless the requirement is explicitly re-scoped.

Purpose (explicit scope, supersedes the earlier "not agent-specific" limit): RDD exists to (1) keep a loop's original direction when context fades, through an anchor held outside anyone's memory, and (2) guarantee autonomy for changes that stay inside the requirement, so only boundary events need a decision. Delegation to AI agents is the strongest motivating case and may shape the rules, but every rule must stay meaningful for human developers facing the same context loss and delegation. The maintainer does not expect external readers; the repository is for people who share this purpose.

## Context To Read

- Start with `README.md`.
- `README.ko.md` is a short Korean overview only; the English documents are the sole source of truth.
- Treat the English public documents under `docs/` as the canonical public structure.

## Documentation Roles

- `README.md`: public English overview and repository structure.
- `README.ko.md`: short public Korean overview linking to the English docs.
- `docs/`: public methodology, loop model, review method, examples, and AI-agent usage.
- `examples/`: public worked examples.
- `templates/`: public templates for PRs and Codex prompts.

Do not add a separate `docs/SPEC.md` unless the existing README/docs split stops being enough to represent current public truth. Avoid duplicating current truth across multiple documents.

## Editing Rules

- Write and maintain public documentation, examples, and templates in English only. Do not add Korean companions. Update `README.ko.md` only when the overview's pointers or core claims become wrong.
- Review documentation changes manually for consistency with the vocabulary, lifecycle, and non-goals below.
- Keep need, goal, requirement, spec, test, implementation, review, loop boundary, and non-goal terminology consistent across docs, examples, templates, skills, and tooling. Preserve the explicit RDD vocabulary mapping in `docs/01-methodology.md`.
- Preserve the requirement-validity lifecycle across public surfaces: distinguish loop-local requirements, durable requirements, and temporary/scoped policies; require assumptions and observable revisit signals for durable requirements; require expiration rules for temporary/scoped policies; and propagate explicit retain/narrow/supersede/discard decisions when revalidation occurs.
- Preserve numeric `R0`/`R1` compatibility when documenting or tooling semantic `ROOT-REQ-*`/`REQ-*` identifiers. Keep semantic adoption and loop-record retention optional, and document explicit old-to-new mappings for identifier migrations.
- Keep changes scoped to the current requirement. If the requirement changes, explicitly re-scope the work instead of quietly expanding adjacent docs.
- Do not put private task manager IDs, operator notes, or private planning details into tracked public files.
- Do not accumulate completed work logs in public docs.
