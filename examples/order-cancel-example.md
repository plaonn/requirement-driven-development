# Order Cancellation Example

## Need and goal context

Users sometimes place an order by mistake or change their decision before fulfillment commitment. The goal is to preserve user control without requiring fulfillment rollback.

## Requirement

Users can cancel an order before fulfillment starts.

## Requirement validity

- Validity scope: Durable.
- Assumptions: Fulfillment start is a reliable operational boundary, and cancellation before that boundary remains permitted.
- Revisit when: The order lifecycle, fulfillment boundary, legal obligation, or refund policy changes.

## Spec

- Orders before fulfillment can be canceled.
- Orders already in fulfillment cannot be canceled.
- Paid orders trigger refund handling.
- Used coupons are restored according to coupon policy.
- Cancellation is idempotent or returns a clear already-canceled result.

## Tests

- Cancel an unpaid order before fulfillment.
- Cancel a paid order before fulfillment and create a refund request.
- Reject cancellation after fulfillment starts.
- Do not duplicate refund on repeated cancellation.

## Implementation notes

The implementation should make the fulfillment boundary explicit and check it before mutating order state.

Refund creation should be tied to successful cancellation of a paid order. Repeated cancellation should not duplicate refund requests.

Coupon restoration should follow existing coupon policy rather than inventing a new promotion rule inside the cancellation loop.

## Review focus

- Is the fulfillment boundary clear?
- Are refund and coupon effects tied to cancellation rules?
- Are repeated cancellation attempts handled safely?
- Did the loop avoid expanding into order editing or fulfillment rollback?

## Requirement change examples

If the real need becomes "users can edit orders before fulfillment," that is a new or re-scoped requirement.

If only refund or coupon edge cases are clarified, that is spec refinement inside the same loop.
