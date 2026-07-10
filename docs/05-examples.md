# RDD Examples

These examples show how RDD keeps a small development loop traceable.

## Example 1: Order cancellation

### Need and goal context

Users sometimes place an order by mistake or change their decision before fulfillment commitment. The goal is to preserve user control without requiring fulfillment rollback.

### Requirement

Users can cancel an order before fulfillment starts.

### Requirement validity

- Validity scope: Durable.
- Assumptions: Fulfillment start is a reliable operational boundary, and cancellation before that boundary remains permitted.
- Revisit when: The order lifecycle, fulfillment boundary, legal obligation, or refund policy changes.

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

Reviewers should check that the loop satisfies cancellation before fulfillment without expanding into order editing, fulfillment rollback, or broad refund policy redesign.

### What would count as requirement change

If the real need becomes "users can edit orders before fulfillment," that is a new or re-scoped requirement.

If only refund or coupon edge cases are clarified, that is spec refinement inside the same loop.

## Example 2: Receipt formatting refactoring

### Need and goal context

Receipt presentation changes are risky because formatting and pricing are coupled. The goal is to let receipt presentation evolve independently while pricing behavior remains stable.

### Requirement

Isolate receipt formatting from pricing calculation without changing pricing behavior.

### Requirement validity

- Validity scope: Loop-local.
- Assumptions: Pricing behavior and receipt wording are not intended to change in this refactoring loop.
- Revisit when: The task intentionally changes pricing behavior or receipt wording; re-scope rather than continuing as a behavior-preserving refactor.

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

If a pricing bug is discovered, open a follow-up instead of hiding it inside the refactoring loop unless the current loop is explicitly re-scoped.
