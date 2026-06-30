# RDD Examples

These examples show how RDD keeps a small development loop traceable.

## Example 1: Order cancellation

### Requirement

Users can cancel an order before fulfillment starts.

### Spec

- Orders before fulfillment can be canceled.
- Orders already in fulfillment cannot be canceled.
- Paid orders trigger refund handling.
- Used coupons are restored according to coupon policy.
- Cancellation is idempotent or returns a clear already-canceled result.

### Tests

- Cancel an unpaid order before fulfillment.
- Cancel a paid order before fulfillment and create a refund request.
- Reject cancellation after fulfillment starts.
- Do not duplicate refund on repeated cancellation.

### Implementation notes

The implementation should keep the fulfillment boundary explicit. Refund and coupon handling should be connected to cancellation rules, not added as unrelated payment or promotion changes.

### Review focus

Reviewers should check that the PR satisfies cancellation before fulfillment without expanding into order editing, fulfillment rollback, or broad refund policy redesign.

### What would count as requirement change

If the real need becomes "users can edit orders before fulfillment," that is a new or re-scoped requirement.

If only refund or coupon edge cases are clarified, that is spec refinement inside the same loop.

## Example 2: Receipt formatting refactoring

### Requirement

Isolate receipt formatting from pricing calculation without changing pricing behavior.

### Spec

- Pricing totals remain unchanged.
- Receipt text formatting is moved behind a formatter boundary.
- Existing discount calculation behavior remains unchanged.
- Snapshot or golden master tests protect receipt output where useful.

### Tests

- Existing pricing tests remain unchanged.
- Receipt output snapshot passes before and after refactoring.
- Discount rule tests still pass.

### Implementation notes

The implementation should move formatting responsibilities without changing calculation rules. If pricing code must be touched, reviewers should be able to see that behavior is preserved.

### Review focus

Reviewers should compare behavior before and after the refactor, especially totals, discounts, rounding, and receipt text output.

### What would count as requirement change

If receipt wording changes intentionally, that is a behavior or spec change and should be explicit.

If a pricing bug is discovered, open a follow-up instead of hiding it inside the refactoring PR unless the current loop is explicitly re-scoped.
