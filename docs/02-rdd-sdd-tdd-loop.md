# RDD, SDD, and TDD

RDD, SDD, and TDD operate at different layers of the same development loop.

```text
RDD: Requirement Driven Development
SDD: Spec Driven Development
TDD: Test Driven Development
```

They should not be treated as competitors. RDD places the requirement at the top of the loop, while SDD and TDD provide increasingly concrete feedback mechanisms.

## Layer model

```text
Requirement
  -> Spec
    -> Test
      -> Implementation
```

Each layer answers a different question.

## RDD: requirement as the loop anchor

RDD asks:

```text
Are we still solving the right requirement?
```

The requirement is the loop anchor. It should be stable for the current loop.

If the requirement changes, the loop should be explicitly re-scoped.

## SDD: spec as the contract

SDD asks:

```text
Have we expressed the requirement as clear behavior, rules, and boundaries?
```

Specs are allowed to evolve inside the loop. That is often the point of implementation and review: the team discovers edge cases, missing constraints, and better wording.

Spec refinement does not necessarily mean the requirement changed.

Example:

```text
Requirement:
  Users can cancel an order before fulfillment starts.

Spec refinements:
  - A paid order triggers refund flow.
  - An order in fulfillment cannot be canceled.
  - A restored coupon should not exceed its original validity window.
```

The requirement is stable; the spec becomes sharper.

## TDD: tests as executable feedback

TDD asks:

```text
Can the current spec be proven continuously by executable checks?
```

Tests are not the requirement. They are executable checkpoints derived from the spec.

Tests may change when:

- the spec becomes more precise,
- an edge case is discovered,
- the test was over-specified,
- the implementation design changes while behavior stays stable,
- a better example captures the same rule more clearly.

## What can change inside one loop?

```text
Usually stable:
  Requirement intent

Expected to evolve:
  Spec details
  Test examples
  Implementation structure

Must be made explicit:
  Requirement change
```

## Common failure modes

### Test-driven but not requirement-driven

The tests pass, but the result misses the original requirement.

This often happens when tests are written against an incomplete interpretation of the spec.

### Spec-driven but not requirement-driven

The spec is detailed, but it encodes the wrong user or product need.

This often happens when specification work becomes detached from the original requirement.

### Implementation-driven loop

The implementation starts shaping the purpose of the PR.

This often creates hidden scope creep: useful-looking changes enter the PR without being connected to the loop requirement.

## RDD's practical stance

RDD does not say specs and tests are less important.

It says they should remain traceable to the requirement that defines the loop.
