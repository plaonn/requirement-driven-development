# RDD 예시

이 예시들은 RDD가 작은 개발 루프를 어떻게 추적 가능하게 유지하는지 보여줍니다.

## 예시 1: 주문 취소

### Requirement

사용자는 fulfillment가 시작되기 전 order를 cancel할 수 있습니다.

### Spec

- Fulfillment 전 order는 cancel할 수 있습니다.
- Fulfillment가 이미 시작된 order는 cancel할 수 없습니다.
- Paid order는 refund handling을 trigger합니다.
- 사용된 coupon은 coupon policy에 따라 복원됩니다.
- Cancellation은 멱등적이거나 명확한 already-canceled result를 반환합니다.

### Tests

- Fulfillment 전 unpaid order cancel
- Fulfillment 전 paid order cancel과 refund request 생성
- Fulfillment 시작 후 cancellation reject
- 반복 cancellation에서 refund 중복 생성 방지

### 구현 참고

Implementation은 fulfillment 경계를 명확히 유지해야 합니다. Refund와 coupon handling은 cancellation 규칙에 연결되어야 하며, 별도 payment 또는 promotion 변경으로 확장되면 안 됩니다.

### 리뷰 초점

Reviewer는 loop가 order editing, fulfillment rollback, refund policy 재설계로 확장되지 않고 fulfillment 전 cancellation을 만족하는지 확인해야 합니다.

### Requirement 변경에 해당하는 것

실제 필요가 "사용자가 fulfillment 전 order를 edit할 수 있음"으로 바뀌면 새 requirement 또는 re-scoped requirement입니다.

Refund 또는 coupon edge case만 명확해지는 것은 같은 루프 안의 spec refinement입니다.

## 예시 2: 영수증 포맷팅 리팩터링

### Requirement

Pricing 동작을 바꾸지 않고 receipt formatting을 pricing calculation에서 분리합니다.

### Spec

- Pricing totals는 그대로 유지됩니다.
- 영수증 텍스트 포맷팅은 formatter 경계 뒤로 이동합니다.
- 기존 discount 계산 동작은 유지됩니다.
- 유용한 경우 snapshot 또는 golden master test가 receipt output을 보호합니다.

### Tests

- 기존 pricing tests 유지
- 리팩터링 전후 영수증 출력 snapshot 통과
- Discount rule tests 통과

### 구현 참고

Implementation은 외부에서 보이는 pricing 동작을 유지하면서 receipt formatting 책임을 분리해야 합니다.

### 리뷰 초점

Reviewer는 totals, discounts, rounding, 영수증 텍스트 출력의 전후 동작을 비교해야 합니다.

### Requirement 변경에 해당하는 것

Receipt wording을 의도적으로 바꾸면 동작 또는 spec 변경이므로 명시해야 합니다.

Pricing bug를 발견했다면 현재 loop를 명시적으로 re-scope하지 않는 한 refactoring loop에 숨기지 말고 follow-up을 엽니다.
