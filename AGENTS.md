# Project Instructions

## Project Purpose

This repository documents Requirement Driven Development (RDD), a lightweight methodology for keeping small development loops traceable from requirement to spec, tests, implementation, and review.

Preserve the repository's public role as a methodology/documentation project. Do not turn it into a project-management tool, framework, or agent-specific workflow unless the requirement is explicitly re-scoped.

## Context To Read

- Start with `README.md`.
- Use `README.ko.md` as the Korean companion overview.
- Treat the English public documents under `docs/` as the canonical public structure.
- Treat `docs/ko/` as Korean companion documentation.

## Documentation Roles

- `README.md`: public English overview and repository structure.
- `README.ko.md`: public Korean companion overview.
- `docs/`: public methodology, loop model, review method, examples, and AI-agent usage.
- `examples/`: public worked examples.
- `templates/`: public templates for PRs and Codex prompts.

Do not add a separate `docs/SPEC.md` unless the existing README/docs split stops being enough to represent current public truth. Avoid duplicating current truth across multiple documents.

## Editing Rules

- Keep English docs as the canonical public structure. Update Korean companion docs when a public English change affects reader-facing meaning.
- Keep requirement, spec, test, implementation, review, loop boundary, and non-goal terminology consistent across docs and templates.
- Keep changes scoped to the current requirement. If the requirement changes, explicitly re-scope the work instead of quietly expanding adjacent docs.
- Do not put private task manager IDs, operator notes, or private planning details into tracked public files.
- Do not accumulate completed work logs in public docs.
