# RDD Methodology

Requirement Driven Development (RDD) is a lightweight methodology for keeping small development loops aligned with their driving requirement.

RDD is based on a simple claim:

```text
A development loop is healthy when its requirement, spec, implementation, acceptance evidence, and review remain traceable to each other.
```

Artifact and documentation ceremony may scale with the size and abstraction level of the work. The minimum semantic trace from a stable requirement to observable evidence remains invariant.

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

The following are normally refinement inside the same requirement when they preserve the same external contract:

```text
  Internal architecture
  Internal APIs or data structures
  Test strategy or test location
  Acceptance refinement that makes the same requirement more precise
  Bounded refactoring
```

The following are loop-boundary changes when they materially change what must be true:

```text
  The capability itself, applicable actor, or scope
  Trigger condition or obligation level
  Accepted failure mode or user-facing behavior
  Authority, security, or privacy boundary
  Another public or cross-system contract
```

The first group may change the spec, tests, or implementation without a new approval boundary. The second group requires explicit re-scoping under the existing RDD rules.

A requirement can be wrong. A requirement can be incomplete. A requirement can change after learning.

RDD does not deny that. It only says that when the requirement changes, the loop boundary has changed too. That change should be explicit.

## Autonomy inside the boundary

The loop boundary is also a delegation contract. Work inside the boundary proceeds without asking for approval. Work that crosses the boundary, or passes a stated automation boundary, stops for a decision by whoever owns the requirement.

This is what makes it safe to leave a loop unattended, whether the worker is a person or an agent. The owner does not review every refinement, only boundary events. The contract fails in both directions: silently expanding past the boundary breaks it, and asking for approval on refinements inside the boundary breaks it too. A stop should name the boundary event that caused it, not general uncertainty about implementation.

## Keeping the anchor across context loss

Long loops, interruptions, handoffs, and context compaction all make the original intent fade. The requirement is the anchor that lives outside anyone's memory.

- **Short enough to reread whole.** The anchor holds the root goal, the current requirement, `Done when`, non-goals, and the automation boundary. If the requirements document is larger than can be read in full at each checkpoint, keep a short anchor at its top (root goal and a map of requirements) and load detailed sections only for the requirements the loop touches.
- **Reread at checkpoints.** Reread the anchor when resuming after an interruption, receiving a handoff, recovering from context compaction, changing phase, and before declaring done.
- **Compare, then classify.** On each reread, compare the current work to the anchor. Divergence is either refinement inside the boundary (continue) or a boundary event (stop and re-scope).
- **Do not use conversation memory as the source.** If the anchor exists only in a conversation, write it down at the start of any loop expected to outlive that context.

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

## Minimum requirement quality

For RDD, a requirement is a useful loop anchor when it has these properties:

```text
Stable:
  It remains the same stakeholder contract while internal architecture, APIs,
  data structures, spec refinement, or test strategy changes.

Normative:
  It is a condition that must be true to call the loop complete.

Discriminating:
  Available evidence can meaningfully classify it as satisfied, unsatisfied,
  or unknown. Unknown is not satisfied.

Solution-independent:
  It does not prescribe a filename, internal API, command, implementation
  strategy, or test location unless that detail is itself part of the external
  contract.
```

Avoid a slogan that cannot be judged and avoid a solution detail disguised as a requirement. If one broad sentence hides several independently verifiable obligations, split it into a small number of atomic requirements. A requirement may be concise; it must still let a reviewer say what evidence would count, what would fail, and what remains unknown.

A Goal or Outcome explains why the loop exists and the desired direction; it is not a discriminating Requirement by itself. The Requirement states the condition that must be true.

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

#### Requirement identifiers and migration

Requirement identifiers are references, not a new RDD layer. RDD supports numeric and semantic representations:

```text
Numeric representation:
  R0, R1, R2, ...

Semantic root requirement:
  ROOT-REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*

Semantic child requirement:
  REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*
```

Numeric hierarchies remain valid. A project does not need to migrate merely because semantic identifiers are available. In semantic mode, exactly one `ROOT-REQ-*` entry has `Parent: none`; every `REQ-*` entry names an existing `ROOT-REQ-*` or `REQ-*` parent. The root requirement may link to a `Root goal`, but the goal remains justification context and is not interchangeable with the requirement.

Use one primary representation inside a requirement hierarchy. General trace extraction may encounter numeric and semantic hierarchies in different documents, but a single source-of-truth hierarchy should not mix them casually.

Once a semantic identifier becomes current truth, do not silently rename, reuse, or renumber it. Existing numeric projects may remain numeric, adopt semantic identifiers only for a separate new hierarchy, or migrate a hierarchy in one explicit reviewable change. An explicit migration records old-to-new mappings such as `Previous identifiers: R1`, updates current parent and active-loop references to the new primary identifiers, and reserves old identifiers from reuse. Historical records may retain their original references. Read-only tooling may validate or report the mapping; it should not rewrite source documents or perform the migration automatically.

### Spec

The spec operationalizes the requirement as rules, contracts, boundaries, and acceptance criteria. In this methodology, `spec` means this loop-level precision layer; it does not mean that a requirements engineering artifact named "requirements specification" must be split or renamed.

Specs may evolve inside the loop as the team learns more about the requirement.

Acceptance criteria describe what evidence would count. They are not the evidence itself.

### Test and acceptance evidence

Tests make parts of the spec executable, but tests are not the only possible evidence. Acceptance evidence may also be a manual check, document comparison, review observation, or other observable result that directly bears on the requirement.

Tests and other evidence are not the requirement itself. They are protection and observation mechanisms for the current interpretation of the spec. Evidence must be strong enough to distinguish `satisfied`, `unsatisfied`, and `unknown`; missing or indirect evidence leaves the requirement `unknown`, not satisfied.

### Implementation

Implementation is the code or document change chosen to realize the current spec and original requirement.

Passing tests is necessary but not sufficient if the implementation violates the requirement's intent or expands beyond the loop boundary. Implementation progress, a passing test suite, a commit, or a task marked complete is delivery hygiene, not direct requirement evidence unless it actually observes the required condition.

### Review

Review checks the full trace in both directions:

```text
Need / Goal -> Requirement -> Spec / Acceptance -> Implementation / Evidence

Implementation / Evidence -> Spec / Acceptance -> Requirement -> Goal / Outcome
```

A good review asks not only whether the code works, but whether the evidence directly supports the requirement, whether unknown remains unresolved, and whether the work still belongs to the current loop. The reverse trace is conceptual guidance, not an agent-specific runtime protocol or mandatory tool sequence.

## Core rule

```text
Spec and test refinement may happen inside the loop.
Requirement change must be made explicit as a loop boundary change.
Artifact ceremony may scale; the minimum Requirement-to-evidence trace remains.
```

This is the practical center of RDD.
