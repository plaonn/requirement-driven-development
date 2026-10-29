# RDD with AI Coding Agents

AI coding agents are the strongest motivating case for RDD. They lose context to compaction and handoff, and they follow implementation momentum into adjacent work unless the loop boundary is explicit. The rules below apply the general rules in [RDD Methodology](01-methodology.md#autonomy-inside-the-boundary) and [Keeping the anchor across context loss](01-methodology.md#keeping-the-anchor-across-context-loss); they are meant to stay meaningful for human developers too.

## Agent loop boundary

When using an agent, give it a stable requirement, explicit spec, acceptance boundary, and non-goals. The agent must be able to identify what observable evidence would establish the requirement, not just what files or tests to touch.

The agent should be allowed to refine specs and tests only when they still express the same requirement. If the requirement appears to change, the agent should stop and report before expanding scope.

## Autonomy and reloading the anchor

Inside the loop boundary the agent proceeds without asking: refining specs and tests, internal design, bounded refactoring, and acceptance refinement for the same requirement. It stops only for a boundary event or a stated stop condition below.

Keep the anchor where it survives context loss, such as the task note, PR description, or a short file in the repository, not only in the conversation. Instruct the agent to reread it after context compaction, after receiving a handoff, at phase changes, and before reporting done. If the agent cannot find the anchor, that is a stop condition, not a reason to reconstruct it from memory.

## Lightweight agent traces

A small agent loop does not need a separate `REQUIREMENTS.md`, active-loop file, or heavyweight artifact. The minimum semantic trace can remain compact in the task, PR, commit message, or agent final review:

```text
Outcome / Goal:
  The desired state.

Requirement:
  The stable condition that must be true.

Done when / Acceptance:
  The observable evidence that can judge the requirement.
```

These are example operational labels, not a mandatory RDD schema. A larger or higher-risk loop may use a full requirement document, validity lifecycle, decision record, or retained loop artifact. A smaller loop may use one short requirement sentence and one evidence line, as long as the semantic distinction remains visible.

## Useful agent instructions

Give agents instructions in this shape:

```text
Need / goal context:
  The stakeholder problem, desire, or desired outcome that justifies this task.

Requirement:
  The stable capability, quality, constraint, or condition this task must satisfy.
  Include rationale, failure prevented, assumptions, and revisit conditions when the requirement may outlive one loop.
  If the task belongs to a larger root goal, state the current narrower stage.

Requirement validity:
  Loop-local requirement, durable requirement, or temporary/scoped policy.
  Durable requirements need assumptions and observable revisit signals.
  Temporary/scoped policies need an expiration rule.

Spec:
  Rules, contracts, acceptance criteria, and boundaries.

Tests:
  Required tests or checks.

Acceptance evidence / Done when:
  The observable result that distinguishes satisfied, unsatisfied, and unknown.

Non-goals:
  Adjacent work that must stay out of scope.

Stop conditions:
  Conditions that require reporting back instead of continuing.

Automation boundary:
  For state-changing work, state what may be automated now, what requires human review, and what should not be automated yet.
```

## Stop conditions

Agents should stop or report when:

- the anchor cannot be found or reread after context loss,
- the root goal, rationale, failure prevented, or automation boundary is unclear enough that deriving a full trace would require guessing,
- the prompt provides a goal or desired outcome but no requirement that states what must be true,
- an assumption has failed or a revisit signal occurred and the requirement has not been revalidated,
- the requirement appears wrong or incomplete,
- implementation suggests an adjacent feature,
- tests need to be changed in a way that alters the requirement,
- no direct acceptance evidence exists for the requirement; report it as `unknown` rather than claiming completion,
- a discovered bug belongs to a different requirement,
- non-goals appear necessary to complete the task,
- the requested change requires a broader architecture or API decision.

When this happens, the agent should use boundary clarification: ask the smallest set of questions needed to settle the loop boundary before continuing.

Implementation or test refinement is not automatically a boundary change. Internal architecture, internal APIs or data structures, test strategy or location, acceptance refinement for the same requirement, and bounded refactoring may stay inside the loop. A material change to capability, actor or scope, trigger, obligation, accepted failure mode, user-facing behavior, authority, security/privacy boundary, or public contract requires re-scoping.

After a revisit signal, the agent should not silently keep using the requirement. It should report the evidence, request or recover a `retain`, `narrow`, `supersede`, or `discard` decision, and identify affected specs, tests, implementation, docs, and active loops.

## Scope discipline

An agent should not expand scope just because implementation suggests adjacent work.

Passing tests, a commit, or a task marked complete are not requirement satisfaction unless they provide direct evidence for the required condition. If evidence cannot distinguish satisfaction from non-satisfaction, report `unknown` rather than closing the loop.

Examples:

- A cancellation task should not become order editing.
- A refactoring task should not hide behavior changes.
- A bug fix should not redesign a related workflow unless explicitly re-scoped.

## Final trace

At the end of the task, the agent should summarize:

```text
Requirement -> Spec / acceptance -> Tests/Checks -> Implementation / evidence

Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```

That final trace helps reviewers decide whether the work stayed inside the loop and whether local implementation progress was traced back to the original requirement. The reverse direction is review guidance, not an agent-specific runtime protocol or mandatory tool call.

In a workflow without pull requests, this final trace can also serve as the review surface for the task or change set. It should be compact enough to read often, but explicit enough to show whether the agent changed the requirement, refined the spec, or found follow-up work that belongs to another loop.
