# Retroactive RDD Review

Retroactive RDD review applies Requirement Driven Development to a project that was not necessarily built with RDD from the start.

Its purpose is not to declare the project "RDD applied." Its purpose is to recover candidate requirements, identify trace gaps, and decide what can safely become current project truth.

## When to use it

Use retroactive review when:

- an existing project has specs, tests, docs, or implementation behavior but unclear driving requirements,
- a team wants to adopt RDD without rewriting history,
- a reviewer needs to distinguish durable requirements from implementation choices,
- a safety or automation boundary appears to exist but its rationale is not documented,
- a project wants a candidate requirement index before writing source-of-truth requirement docs.

## Core rule

```text
Recovered requirements are candidates until confirmed.
```

Existing behavior is evidence, not proof of requirement. Tests are evidence, not proof of product intent. A repeated constraint may be important, but it should not become project truth unless its purpose, rationale, and failure prevented are recoverable or confirmed.

## Review sequence

1. Read current truth.
   Start with current docs, specs, tests, public contracts, safety notes, and active task surfaces. Prefer current truth over old roadmap notes or completed work logs.

2. Inventory existing claims.
   Extract explicit specs, invariants, acceptance criteria, non-goals, safety defaults, and repeated constraints. Keep implementation facts separate from stated behavior contracts.

3. Infer candidate requirements.
   Ask what user, product, business, operational, safety, or technical need each important spec appears to protect. A useful candidate requirement explains why the behavior matters, not only what the system does.

4. Mark confidence.
   Use explicit confidence labels:

   ```text
   confirmed:
     Directly stated by current docs, tests, or user confirmation.

   inferred:
     Strongly implied by current behavior, tests, or repeated constraints, but not directly stated.

   unclear:
     Plausible but under-evidenced.
   ```

5. Separate change risk.

   ```text
   change-dangerous:
     The spec appears to protect an active requirement or safety invariant.

   change-review-needed:
     The spec is linked to an inferred requirement or unresolved assumption.

   change-likely-safe:
     The behavior appears to be an implementation choice rather than product intent.
   ```

   Missing traceability is review-needed, not automatically safe.

## Boundary Questions First

For projects with substantial pre-RDD history, a full requirement hierarchy is often premature.

Use boundary clarification before producing a hierarchy when these are unclear:

- the root goal the recovered requirements serve,
- the rationale or failure prevented,
- whether a constraint is durable requirement or implementation choice,
- the automation boundary for state-changing work,
- whether the user wants read-only review, a candidate index, confirmed project truth, or only forward RDD for future loops.

Use this compact form:

```text
Boundary Questions First
- Why this is needed:
- Known trace:
- Questions:
  1. ...
- What will be classified after answers:
```

## Retroactive coverage

Before promoting recovered requirements into source-of-truth docs, summarize coverage:

```text
Retroactive Coverage
- Adoption scope:
- What appears already traceable:
- What is inferred but not confirmed:
- Specs/tests without recovered rationale:
- What should not be called RDD-applied yet:
```

This prevents a first-pass review from being mistaken for full adoption.

## Candidate requirement shape

When enough evidence exists, use this shape:

```text
Candidate Requirement
- Title:
  Status: confirmed | inferred | unclear
  Requirement:
  Rationale:
  Failure prevented:
  Assumptions:
  Derived specs/tests:
  Evidence:
  Revisit when:
```

If rationale, failure prevented, or assumptions cannot be recovered, keep the item as an unresolved candidate or trace gap.

## Adoption boundary

Retroactive review and requirement adoption are different loops.

Retroactive review may produce:

- a coverage summary,
- candidate requirements,
- trace gaps,
- confirmation questions,
- change-risk guidance.

It should not silently produce:

- a completed requirement set,
- source-of-truth project requirements,
- public docs that imply confirmed adoption,
- implementation changes,
- automation policy changes.

Promoting a candidate requirement into project truth should be a separate forward RDD loop with its own requirement, rationale, failure prevented, review, and non-goals.

## Review output

A compact retroactive review can use:

```text
Root Goal
- Goal:
  Status:
  Rationale:
  Evidence:

Candidate Requirements
- R?: ...

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
  Change risk:
  Notes:

Open Questions
1. ...

Implementation Choices
- Likely safe to change, assuming the candidate requirements remain satisfied:
```

Keep the report small enough to review. Expand only the parts needed for the next decision.

## Guardrails

- Do not treat every existing behavior as a requirement.
- Do not treat every test as proof of product intent.
- Do not treat a first-pass candidate hierarchy as proof that the project now satisfies RDD.
- Do not call recovered requirements current truth unless confirmed.
- Do not convert retroactive candidates into public source-of-truth docs without a separate adoption loop.
- Do not let implementation convenience redefine the requirement.
- Do not erase uncertainty.
