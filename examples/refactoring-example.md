# Receipt Formatting Refactoring Example

## Need and goal context

Receipt presentation changes are risky because formatting and pricing are coupled. The goal is to let receipt presentation evolve independently while pricing behavior remains stable.

## Requirement

Isolate receipt formatting from pricing calculation without changing pricing behavior.

## Requirement validity

- Validity scope: Loop-local.
- Assumptions: Pricing behavior and receipt wording are not intended to change in this refactoring loop.
- Revisit when: The task intentionally changes pricing behavior or receipt wording; re-scope rather than continuing as a behavior-preserving refactor.

## Spec

- Pricing totals remain unchanged.
- Receipt text formatting is moved behind a formatter boundary.
- Existing discount calculation behavior remains unchanged.
- Snapshot or golden master tests protect output where useful.

## Tests

- Existing pricing tests remain unchanged.
- Receipt output snapshot passes before and after refactoring.
- Discount rules still pass.

## Implementation notes

The implementation should separate receipt formatting from pricing calculation while preserving externally visible pricing behavior.

If code movement touches pricing paths, tests should show that totals, discounts, rounding, and receipt output remain stable.

## Review focus

- Did formatting move behind a clear boundary?
- Did pricing behavior remain unchanged?
- Are any receipt wording changes intentional and documented?
- Did the loop avoid hiding bug fixes inside a refactoring loop?

## Requirement change examples

If receipt wording changes intentionally, that is a behavior or spec change and should be explicit.

If a pricing bug is discovered, open a follow-up instead of hiding it inside the refactoring loop unless explicitly re-scoped.
