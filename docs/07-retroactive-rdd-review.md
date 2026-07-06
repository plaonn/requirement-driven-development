# Retroactive RDD Review

Retroactive RDD review applies Requirement Driven Development to a project that was not necessarily built with RDD from the start.

Its purpose is not to declare the project "RDD applied." Its purpose is to recover candidate requirements, identify trace gaps, and decide what can safely become current project truth.

## When to use it

Use retroactive review when:

- an existing project has specs, tests, docs, or implementation behavior but unclear driving requirements,
- a team wants to adopt RDD without rewriting history,
- a reviewer needs to distinguish durable requirements from temporary policies, provider workarounds, and implementation choices,
- a safety or automation boundary appears to exist but its rationale is not documented,
- a project wants a candidate requirement index before writing source-of-truth requirement docs.

## Core rule

```text
Recovered requirements are candidates until confirmed.
```

Existing behavior is evidence, not proof of requirement. Tests are evidence, not proof of product intent. A repeated constraint may be important, but it should not become project truth unless its purpose, rationale, and failure prevented are recoverable or confirmed.

Not every confirmed or accepted decision is a system-wide requirement. A review may confirm that a temporary experiment policy, provider workaround, or operator-run-specific risk decision is valid for its scope while still keeping it out of the durable requirement set.

## Review sequence

1. Read current truth.
   Start with current docs, specs, tests, public contracts, safety notes, and active task surfaces. Prefer current truth over old roadmap notes or completed work logs.

2. Inventory existing claims.
   Extract explicit specs, invariants, acceptance criteria, non-goals, safety defaults, policies, workarounds, and repeated constraints. Keep implementation facts separate from stated behavior contracts.

3. Classify decisions before promotion.
   Mark each important decision as one of:

   ```text
   Durable Requirement
   Temporary Experiment Policy
   Provider Workaround
   Implementation Choice
   Promotion Candidate
   Expired/Superseded Policy
   ```

   If a decision is marked `accepted`, record whether that means system-wide requirement accepted, beta-only policy accepted, operator-run-specific risk accepted, or code-unlock condition accepted but implementation blocked.

4. Infer candidate requirements.
   Ask what user, product, business, operational, safety, or technical need each important spec appears to protect. A useful candidate requirement explains why the behavior matters, not only what the system does.

5. Mark confidence.
   Use explicit confidence labels:

   ```text
   confirmed:
     Directly stated by current docs, tests, or user confirmation.

   inferred:
     Strongly implied by current behavior, tests, or repeated constraints, but not directly stated.

   unclear:
     Plausible but under-evidenced.
   ```

6. Separate change risk.

   ```text
   change-dangerous:
     The spec appears to protect an active requirement or safety invariant.

   change-review-needed:
     The spec is linked to an inferred requirement or unresolved assumption.

   change-likely-safe:
     The behavior appears to be an implementation choice rather than product intent.
   ```

   Missing traceability is review-needed, not automatically safe.

## Policy and promotion boundary

Temporary policies are valid RDD records. They should be recorded with enough lifecycle context that future readers do not mistake them for permanent requirements.

Use fields like:

```text
Decision class:
Durability:
Acceptance scope:
Policy horizon:
Promotion rule:
Expiration rule:
Canonical owner:
```

Promote a policy toward a durable requirement when it repeatedly applies across experiments, prevents financial, security, safety, or external side effects if violated, survives provider changes, affects multiple implementation surfaces, or requires operator flow and tests to move together.

Keep it as policy when it is tied to a specific symbol, amount, market, provider app check result, beta/live-test convenience, limited date range, or one or two experiments that may be discarded.

## Boundary Questions First

For projects with substantial pre-RDD history, a full requirement hierarchy is often premature.

When someone asks to review an existing project "from an RDD perspective" or to
apply RDD broadly, do not start with a normal findings-first code review. Start
with Boundary Questions First unless the user explicitly asked only for a
read-only candidate index or implementation risk audit.

Use boundary clarification before producing a hierarchy when these are unclear:

- the root goal the recovered requirements serve,
- the rationale or failure prevented,
- whether a constraint is durable requirement, temporary policy, provider workaround, or implementation choice,
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

## Stale proposal detection

Retroactive review should also look for old decisions that now read like current policy.

Ask:

- Does an old proposal read like an active policy?
- Does a blocked decision still look active in the roadmap?
- Does a README example behave differently from the current spec?
- Does a disabled path look enabled in the docs?

If yes, classify the item before editing it. It may need promotion, expiration, superseding, or relocation to a policy record instead of becoming a durable requirement.

## Candidate requirement shape

When enough evidence exists, use this shape:

```text
Candidate Requirement
- Title:
  Status: confirmed | inferred | unclear
  Decision class: Durable Requirement
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
- classified temporary policies or provider workarounds,
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

Decision Register
- D?: ...
  Decision class:
  Durability:
  Acceptance scope:
  Policy horizon:
  Promotion rule:
  Expiration rule:
  Canonical owner:

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

Stale Proposal Checks
- Old proposal/current-policy confusion:
- Blocked decision still active:
- README/spec behavior mismatch:
- Disabled path documented as enabled:
```

Keep the report small enough to review. Expand only the parts needed for the next decision.

## Guardrails

- Do not treat every existing behavior as a requirement.
- Do not treat every test as proof of product intent.
- Do not treat a first-pass candidate hierarchy as proof that the project now satisfies RDD.
- Do not call recovered requirements current truth unless confirmed.
- Do not convert retroactive candidates into public source-of-truth docs without a separate adoption loop.
- Do not promote temporary experiment policies, provider workarounds, or operator-run risk decisions into durable requirements without a promotion rule.
- Do not let implementation convenience redefine the requirement.
- Do not erase uncertainty.
