# Receipt Formatting Refactoring Example

## Need and goal context

Receipt presentation changes are risky because formatting and pricing are coupled. The goal is to let receipt presentation evolve independently while pricing behavior remains stable.

In this example, the user asks the team to separate formatting from pricing across the project while preserving charged amounts and receipt text. The team chooses a formatter and snapshot tests. A successor may replace either choice within that assignment.

## Requirement

Receipt formatting can evolve independently of pricing. This refactor preserves pricing behavior and receipt text.

## Requirement validity

- Validity scope: Loop-local.
- Assumptions: The current pricing rules and receipt format still apply.
- Revisit when: The task intentionally changes pricing behavior or receipt wording; re-scope rather than continuing as a behavior-preserving refactor.

## Spec

- Pricing totals remain unchanged.
- Receipt text formatting is moved behind a formatter boundary.
- Existing discount calculation behavior remains unchanged.
- Snapshot or golden master tests protect output where useful.

## Tests

- Compare totals for the same orders before and after the change, including discounted orders and rounding boundaries.
- Compare receipt text for those orders. The team uses snapshots for this comparison.

## Implementation notes

The implementation should separate receipt formatting from pricing calculation while preserving externally visible pricing behavior.

If code movement touches pricing paths, tests should show that totals, discounts, rounding, and receipt output remain stable.

## Review focus

- Did formatting move behind a clear boundary?
- Did pricing behavior remain unchanged?
- Does the receipt text match the pre-refactor output?
- Did the loop avoid hiding bug fixes inside a refactoring loop?

## Requirement change examples

Changing a module boundary while preserving charged amounts and receipt text stays within this assignment. Changing the amount charged at a rounding boundary or intentionally changing receipt wording requires a decision from the requirement owner.

If a pricing bug is discovered, open a follow-up instead of hiding it inside the refactoring loop unless explicitly re-scoped.
