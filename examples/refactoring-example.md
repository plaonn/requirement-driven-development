# Receipt Formatting Refactoring Example

## Requirement

Isolate receipt formatting from pricing calculation without changing pricing behavior.

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
- Did the PR avoid hiding bug fixes inside a refactoring loop?

## Requirement change examples

If receipt wording changes intentionally, that is a behavior or spec change and should be explicit.

If a pricing bug is discovered, open a follow-up instead of hiding it inside the refactoring PR unless explicitly re-scoped.
