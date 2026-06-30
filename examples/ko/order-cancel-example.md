# 주문 취소 예시

## Requirement

사용자는 fulfillment가 시작되기 전 order를 cancel할 수 있습니다.

## Spec

- Fulfillment 전 order는 cancel할 수 있습니다.
- Fulfillment가 이미 시작된 order는 cancel할 수 없습니다.
- Paid order는 refund handling을 trigger합니다.
- 사용된 coupon은 coupon policy에 따라 복원됩니다.
- Cancellation은 idempotent이거나 명확한 already-canceled result를 반환합니다.

## Tests

- Fulfillment 전 unpaid order cancel
- Fulfillment 전 paid order cancel과 refund request 생성
- Fulfillment 시작 후 cancellation reject
- Repeated cancellation에서 refund 중복 생성 방지

## Implementation notes

Implementation은 order state를 바꾸기 전에 fulfillment boundary를 명확히 확인해야 합니다.

Refund creation은 paid order의 successful cancellation과 연결되어야 합니다. Repeated cancellation은 refund request를 중복 생성하면 안 됩니다.

Coupon restoration은 cancellation loop 안에서 새 promotion rule을 만들지 말고 기존 coupon policy를 따라야 합니다.

## Review focus

- Fulfillment boundary가 명확한가?
- Refund와 coupon effect가 cancellation rule에 연결되어 있는가?
- Repeated cancellation attempt가 안전하게 처리되는가?
- PR이 order editing 또는 fulfillment rollback으로 확장되지 않았는가?

## Requirement change examples

실제 필요가 "사용자가 fulfillment 전 order를 edit할 수 있음"으로 바뀌면 새 requirement 또는 re-scoped requirement입니다.

Refund 또는 coupon edge case만 명확해지는 것은 같은 loop 안의 spec refinement입니다.
