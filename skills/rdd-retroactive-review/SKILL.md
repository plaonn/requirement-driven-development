---
name: rdd-retroactive-review
description: Review an existing project through RDD by recovering candidate requirements from current docs, specs, tests, implementation behavior, safety invariants, or task notes. Use when asked to apply RDD retroactively, reconstruct requirements, distinguish durable requirements from implementation choices, find trace gaps, or produce confirmation questions before changing code or docs.
---

# RDD Retroactive Review

## Purpose

Use this skill to work backward from an existing project's current truth to candidate requirements.

This is not forward planning. Do not invent a requirement and push the project toward it. Start from current docs, specs, tests, implementation behavior, and safety invariants, then recover what requirements appear to explain them.

For projects with substantial pre-RDD history, assume the project does not yet satisfy RDD traceability as a whole. A retroactive review can recover candidates and trace gaps, but it must not imply that the historical project is now "RDD applied" or that the recovered requirements are complete.

For the general method, use `docs/07-retroactive-rdd-review.md` as the public source.

## Default Mode

Default to read-only review.

Do not edit files, commit, push, complete tasks, or change external state unless the user explicitly asks for that after seeing the review. If the target repo has stricter local instructions, follow them.

## Output Language

Write developer-facing output in the target project's developer-facing language. Prefer the user's explicit instruction, then target-local instructions, then the language of README/spec/task docs. Keep code identifiers, API names, paths, command names, protocol names, and exact field names unchanged.

## Retroactive Adoption Boundary

When the target project was not originally developed with RDD, default to a coverage review before proposing or editing a durable requirement hierarchy.

- Treat recovered requirements as `candidate`, `inferred`, or `unclear` unless the user explicitly confirms them as current source of truth.
- Do not say the project "now satisfies RDD", "has RDD applied", or "has its requirements set" after a first-pass retroactive review.
- Do not promote inferred requirements into public docs, task dashboards, specs, or source-of-truth requirement files without a separate explicit adoption decision.
- If the user asks to apply RDD broadly, first clarify whether they want read-only coverage review, a candidate requirement index, a confirmed source-of-truth document, or only forward RDD for future loops.
- Documentation changes that turn recovered candidates into project truth are a separate forward RDD loop.

## Workflow

1. Read target-local instructions and current-truth surfaces.
   - Read `AGENTS.md` or equivalent local instructions first when available.
   - Read project docs that define current behavior, especially README, specs, architecture docs, safety docs, task bodies, and relevant tests.
   - Prefer current truth over stale roadmap or completed work logs.
   - Note whether the project appears to have substantial pre-RDD history.

2. Inventory existing claims.
   - Extract explicit specs, invariants, contracts, acceptance criteria, test expectations, non-goals, safety defaults, and repeated constraints.
   - Keep implementation facts separate from stated behavior contracts.

3. Infer candidate requirements.
   - For each important spec or invariant, ask what user, product, operational, safety, or technical need it appears to protect.
   - A candidate requirement must explain who or what benefits, what failure or risk is prevented, and why the constraint matters.
   - Recover the root goal before classifying lower-level requirements when a larger product or operational goal exists.
   - For automation or state-changing work, identify the automation boundary.
   - Mark confidence explicitly:
     - `confirmed`: directly stated by current docs, tests, or user confirmation.
     - `inferred`: strongly implied but not directly stated.
     - `unclear`: plausible but under-evidenced.
   - Do not treat repeated implementation behavior as `confirmed` merely because it exists in code and tests.
   - If purpose cannot be recovered, report a trace gap rather than a complete requirement.

4. Recover rationale and assumptions.
   - Record why the requirement likely matters.
   - Record what would go wrong if the derived spec were removed or weakened.
   - Record assumptions that would make the requirement invalid or worth revisiting.
   - If rationale or assumptions cannot be recovered, ask a question instead of filling the gap with certainty.

5. Separate change risk.
   - `change-dangerous`: appears to protect an active requirement or safety invariant.
   - `change-review-needed`: linked to an inferred requirement or unresolved assumption.
   - `change-likely-safe`: likely implementation structure without product meaning.
   - Treat missing traceability as review-needed, not automatically safe.

6. Use Boundary Questions First when needed.
   - If root goal, rationale, failure prevented, implementation-choice boundary, or automation boundary is central but under-evidenced, do not produce a full hierarchy first.
   - If the project has substantial pre-RDD history and the user asks to "apply RDD" broadly, default to Boundary Questions First unless they explicitly asked only for a draft candidate index.

## Output Contract

Keep reports compact. Expand only areas needed for the user's next decision.

If boundary-critical information is missing:

```text
Boundary Questions First
- Why this is needed:
- Known trace:
- Questions:
  1. ...
- What will be classified after answers:
```

For substantial pre-RDD history, include:

```text
Retroactive Coverage
- Adoption scope:
- What appears already traceable:
- What is inferred but not confirmed:
- Specs/tests without recovered rationale:
- What should not be called RDD-applied yet:
```

Full review shape:

```text
Root Goal
- Goal:
  Status: confirmed | inferred | unclear
  Rationale:
  Evidence:

Candidate Requirements
- R?: [short title]
  Status: confirmed | inferred | unclear
  Requirement:
  Rationale:
  Failure prevented:
  Assumptions:
  Derived specs/tests:
  Evidence:
  Revisit when:

Unresolved Requirement Candidates
- Spec/invariant:
  Possible requirement:
  Missing rationale/assumption:
  Question needed:

Automation Boundary
- Automate now:
- Require human review:
- Do not automate yet:
- Evidence/uncertainty:

Spec Trace
- Spec/invariant:
  Candidate requirement:
  Change risk: change-dangerous | change-review-needed | change-likely-safe
  Notes:

Open Questions
1. ...

Implementation Choices
- Likely safe to change, assuming the candidate requirements remain satisfied:

RDD Observations
- What this review suggests about the RDD workflow, templates, or documentation:
```

## Guardrails

- Do not treat every existing behavior as a requirement.
- Do not treat every test as proof of product intent.
- Do not treat a first-pass candidate hierarchy as proof that the project now satisfies RDD.
- Do not call recovered requirements current truth unless confirmed.
- Do not convert retroactive candidates into public source-of-truth docs without a separate adoption loop.
- Do not output requirements that only say what the system must do.
- If an item has no recoverable rationale, classify it as a traceability gap.
- Do not let a current safety stage erase a broader root goal, and do not let a broad root goal erase the current safety boundary.
- Do not erase uncertainty.
- Do not silently convert a retroactive review into an implementation task.
