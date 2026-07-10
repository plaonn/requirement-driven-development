# RDD Methodology

Requirement Driven Development (RDD) is a lightweight methodology for keeping small development loops aligned with their driving requirement.

RDD is based on a simple claim:

```text
A development loop is healthy when its requirement, spec, tests, implementation, and review remain traceable to each other.
```

## Development loop

A development loop may be a pull request, a task, a ticket, a story, a bug fix, or a small agile iteration.

RDD is intentionally scoped to small loops. It does not try to replace product discovery, roadmap planning, Scrum, Kanban, XP, or TDD. It gives those practices a traceability model for day-to-day development work.

## The loop boundary

In RDD, every loop needs a stable requirement.

That requirement defines the boundary of the loop:

```text
Inside the loop:
  Refining specs
  Adding examples
  Adding tests
  Simplifying implementation
  Clarifying acceptance criteria

Outside the loop:
  Changing the underlying requirement
  Expanding the goal to a different user need
  Mixing unrelated fixes
  Adding opportunistic behavior changes
```

A requirement can be wrong. A requirement can be incomplete. A requirement can change after learning.

RDD does not deny that. It only says that when the requirement changes, the loop boundary has changed too. That change should be explicit.

## Vocabulary boundary

Requirements engineering uses `need`, `goal`, `requirement`, and `specification` in several related ways. For example, a requirement may mean a perceived stakeholder need, a capability or property a system must have, or a documented representation of either. A requirements specification may mean an entire organized collection of requirements.

RDD uses a narrower operational convention so reviewers can distinguish purpose, obligation, interpretation, and solution:

```text
Need:
  A problem, desire, or expected outcome perceived by a stakeholder or found in the operating context.
  Needs may be incomplete, conflicting, or not yet accepted.

Goal:
  A desired state or outcome that gives direction to one or more requirements.
  A root goal may organize several staged development loops.

Requirement:
  A capability, quality, constraint, or other condition that must be satisfied.
  The accepted requirement for the current loop defines its boundary.

Spec:
  The current precise expression of the requirement as rules, contracts, boundaries, and acceptance criteria.
  A spec operationalizes the requirement without turning the current implementation choice into the requirement.

Implementation choice:
  A design, technology, algorithm, structure, or workflow chosen to satisfy the spec and requirement.
```

The relationship is:

```text
Requirements engineering or discovery context:
  Need -> Goal -> Candidate requirement

RDD development loop:
  Accepted loop requirement -> Spec -> Test/Check -> Implementation -> Review
```

The first line is context, not an RDD claim that needs and goals always form a simple linear process. The second line is the development trace RDD controls.

This convention is not a universal redefinition of requirements engineering terminology. When RDD interoperates with an established requirements repository, standard, or domain vocabulary, preserve the external terms and map them explicitly to the RDD layers instead of renaming source artifacts.

## Roles of each layer

### Requirement

The requirement states the capability, quality, constraint, or condition that the loop must satisfy. The linked need, goal, and rationale explain why the work exists.

Good requirements are not always long, but they should be clear enough to distinguish success from unrelated change.

Examples:

```text
Users can cancel an order before fulfillment starts.

The report export should preserve the same filters visible in the UI.

The parser should reject malformed input with actionable errors.

This refactoring should isolate receipt formatting without changing pricing behavior.
```

#### Purpose-bearing requirements

A requirement should preserve its connection to purpose, not only desired behavior. When the need, goal, or rationale is missing, teams often mistake an implementation choice for a durable requirement.

For a requirement that may guide more than one small change, ask:

```text
Root goal:
  What larger desired state or outcome is this loop serving?

Need:
  What stakeholder problem, desire, or expected outcome makes the requirement relevant?

Requirement:
  What capability, quality, constraint, or condition must remain true in this loop?

Rationale:
  Why does this requirement matter now?

Failure prevented:
  What bad outcome, regression, or risk does this requirement prevent?

Assumptions:
  What must be true for this requirement to remain valid?

Revisit when:
  What future signal should cause the team to narrow, supersede, or discard it?
```

The root goal is especially useful when a project has a long-term direction that cannot be implemented safely in one step. For example, a long-term goal may be automation, while the current loop only allows read-only analysis or approval-gated execution. RDD should express that as staged requirements, not as a contradiction.

Automation-heavy loops should also state an automation boundary:

```text
Automate now:
  Work the system may perform without additional review.

Require review:
  Work that may be prepared, but needs explicit human approval.

Do not automate yet:
  Adjacent work that remains out of scope until a later requirement is confirmed.
```

#### Decision classes

RDD should not treat every decision as a durable requirement.

Use a decision class when a rule, limit, workaround, or review condition needs to be recorded but may not deserve promotion into the durable requirement set:

```text
Durable Requirement:
  A product, system, safety, business, or technical capability, quality, constraint, or condition that should keep guiding future loops.

Temporary Experiment Policy:
  A bounded rule for a beta, live test, trial amount, market, date range, operator run, or limited experiment.

Provider Workaround:
  A constraint caused by a specific provider, platform, API, app check, or external dependency behavior.

Implementation Choice:
  A current design or code structure chosen to satisfy the requirement, but not itself the requirement.

Promotion Candidate:
  A repeated policy or workaround that may become a durable requirement if evidence accumulates.

Expired/Superseded Policy:
  A policy that should no longer guide new work except as historical context.
```

The word `accepted` should always carry scope. For example:

```text
Acceptance scope:
  system-wide requirement accepted
  beta-only policy accepted
  operator-run-specific risk accepted
  code-unlock condition accepted but implementation blocked
```

For policy or decision records, useful fields include:

```text
Decision class:
Durability:
Acceptance scope:
Policy horizon:
Promotion rule:
Expiration rule:
Canonical owner:
```

A decision is a stronger candidate for requirement promotion when it applies across multiple experiments, prevents financial, security, safety, or external side effects if violated, remains true across provider changes, affects multiple implementation surfaces, or requires both operator flow and tests to follow it.

Keep a decision as a policy rather than a durable requirement when it applies only to a specific symbol, amount, market, provider check result, beta run, date range, or one or two experiments. Temporary policies are valid RDD artifacts; the risk is letting them read like permanent system requirements without a promotion or expiration rule.

#### Boundary clarification

Sometimes the most useful RDD step is not writing a full trace. It is stopping early to clarify the loop boundary.

Use boundary clarification before deriving specs, tests, or implementation when any of these are unclear:

- the root goal the loop serves,
- the rationale or failure the requirement is meant to prevent,
- whether a constraint is a durable requirement, temporary policy, provider workaround, or implementation choice,
- the automation boundary for state-changing work,
- the current safety stage under a broader long-term goal.

In that case, ask the smallest set of questions needed to confirm, reject, narrow, or supersede the candidate requirement. Do not fill the gap by inventing rationale. Once the boundary is clear, continue with the ordinary RDD trace.

#### Loop requirements and durable requirements

The requirement that defines a development loop is local to that loop, but it does not have to disappear after the loop ends.

Some requirements are only task context. Others become durable product or system requirements that should keep guiding future design changes. When a requirement is meant to stay useful beyond one loop, it should preserve enough context to explain why the constraint exists.

For long-lived requirements, record these fields:

```text
Decision class:
  Durable Requirement.

Validity scope:
  Durable.

Requirement:
  The product, system, safety, business, or technical capability, quality, constraint, or condition that should remain true.

Rationale:
  Why this requirement matters given the linked need and goal.

Failure prevented:
  What would go wrong if the derived spec were removed or weakened.

Assumptions:
  Conditions that make the requirement valid.

Derived specs:
  Current rules or contracts chosen to satisfy the requirement.

Revisit when:
  Conditions under which the requirement should be re-evaluated.
```

The goal is not to turn requirements into long essays. The goal is to keep enough intent that future maintainers can tell which specs protect active requirements and which specs are implementation choices that may change.

A durable requirement set should be curated, not merely accumulated. If a new requirement conflicts with an existing one, the conflict should be resolved explicitly by superseding, narrowing, rejecting, or re-scoping one of them.

#### Requirement validity lifecycle

Requirement stability inside a loop does not mean permanent validity. RDD should preserve enough information to recognize when an existing requirement may no longer be a trustworthy anchor.

Classify its validity scope:

```text
Loop-local requirement:
  Valid for the current development loop.
  The loop boundary is its default lifetime.

Durable requirement:
  Intended to guide future loops.
  Assumptions and observable revisit signals are required.

Temporary/scoped policy:
  A constraint that is valid only for a stated policy horizon, experiment, provider, market, or operating context.
  It should not be promoted into the durable requirement set merely because it currently anchors work.
  An expiration rule is required.
```

For a durable requirement, record:

```text
Validity scope:
  Durable.

Assumptions:
  Conditions that must remain true for the requirement to stay valid.

Revisit when:
  Observable signals that trigger revalidation.
```

Useful revisit signals include an assumption becoming false, the stakeholder need or root goal changing, new evidence defeating the rationale, a law or external dependency changing, a newer accepted requirement conflicting with it, or the derived spec no longer preventing the stated failure.

A revisit signal is not itself an automatic invalidation decision. When a signal is observed:

```text
1. Mark the requirement as under review for affected new work.
2. Revalidate its need, goal, rationale, failure prevented, and assumptions.
3. Decide: retain | narrow | supersede | discard.
4. Record the evidence and replacement requirement when applicable.
5. Propagate the decision to derived specs, tests, implementation, docs, and active loops.
```

The invalidation boundary becomes explicit when revalidation concludes that the requirement no longer serves its linked need or goal, or that its validity assumptions no longer hold. If work is already in progress, that conclusion is a loop-boundary event and the affected loop must be re-scoped, split, or stopped.

#### Requirement document structure

When a project keeps durable requirements in source-of-truth documents, keep the entry point easy to scan. A top-level `REQUIREMENTS.md` can hold the root goal, requirement hierarchy, and links to detail documents.

If one requirement grows enough to need its own rationale, validity conditions, derived specs, tests, decisions, or revisit history, prefer splitting that detail into a narrower document such as `docs/requirements/R1-project-navigation.md`. Keep the index document as the current-truth map rather than turning it into a long discussion archive.

The split point is not raw file length. Split when the document no longer matches the way people or agents need to load context for a task. Do not split a requirement set that must always be read together to understand the active contract.

### Spec

The spec operationalizes the requirement as rules, contracts, boundaries, and acceptance criteria. In this methodology, `spec` means this loop-level precision layer; it does not mean that a requirements engineering artifact named "requirements specification" must be split or renamed.

Specs may evolve inside the loop as the team learns more about the requirement.

### Test

Tests make parts of the spec executable.

Tests are not the requirement itself. They are a protection mechanism for the current interpretation of the spec.

### Implementation

Implementation satisfies the tests and the original requirement.

Passing tests is necessary but not sufficient if the implementation violates the requirement's intent or expands beyond the loop boundary.

### Review

Review checks the full trace:

```text
Requirement -> Spec -> Test -> Implementation
```

A good review asks not only whether the code works, but whether the work still belongs to the current loop.

## Core rule

```text
Spec and test refinement may happen inside the loop.
Requirement change must be made explicit as a loop boundary change.
```

This is the practical center of RDD.
