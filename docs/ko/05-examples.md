# RDD 예시

이 예시들은 RDD가 작은 개발 루프를 어떻게 추적 가능하게 유지하는지 보여줍니다.

## 예시 1: 주문 취소

### Need와 goal context

사용자는 실수로 order를 만들거나 fulfillment commitment 전에 결정을 바꾸기도 합니다. Goal은 fulfillment rollback 없이 사용자 control을 보존하는 것입니다.

### Requirement

사용자는 fulfillment가 시작되기 전 order를 cancel할 수 있습니다.

### Requirement validity

- Validity scope: Durable.
- Assumptions: Fulfillment start가 신뢰할 수 있는 operational boundary이며, 그 boundary 전 cancellation이 계속 허용됩니다.
- Revisit when: Order lifecycle, fulfillment boundary, 법적 의무 또는 refund policy가 바뀔 때입니다.

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

### Need와 goal context

Formatting과 pricing이 결합되어 있어 receipt presentation 변경이 위험합니다. Goal은 pricing behavior를 안정적으로 유지하면서 receipt presentation을 독립적으로 바꿀 수 있게 하는 것입니다.

### Requirement

Pricing 동작을 바꾸지 않고 receipt formatting을 pricing calculation에서 분리합니다.

### Requirement validity

- Validity scope: Loop-local.
- Assumptions: 이 refactoring loop에서는 pricing behavior와 receipt wording을 바꾸지 않습니다.
- Revisit when: Task가 pricing behavior 또는 receipt wording을 의도적으로 바꾸려 할 때이며, behavior-preserving refactor로 계속하지 않고 re-scope합니다.

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

## 예시 3: Implementation-first authority drift

### 초기 상황

기존 integration service에 새 external capability를 지원한다는 broad root requirement가 있습니다. 변경은 OAuth scope와 다른 repository를 통해 write하는 state-changing adapter를 추가합니다. Implementation, test, deployment, behavior spec이 먼저 완료됩니다.

### Trace가 불완전한 이유

Test 통과는 adapter가 spec대로 동작함을 보여 줍니다. 그러나 다음을 확정하지는 않습니다.

- 어느 repository가 state transition의 canonical owner인지
- 이 service가 delegated authority를 행사할 수 있는 이유
- Boundary가 어떤 failure 또는 unauthorized effect를 막는지
- Ownership과 trust-boundary 선택을 decision record로 남겨야 하는지

Broad root requirement는 확장을 허용하지만, 그것만으로 더 좁은 authority boundary를 cover하지는 않습니다.

### 수정된 start gate

- Trigger: 새 OAuth scope, state-changing cross-repository adapter, delegated authority
- Requirement coverage: 허용된 state transition, canonical owner, rationale, failure prevented를 명시하는 더 좁은 durable requirement를 adopt 또는 confirm
- Derived behavior spec: authorization, idempotency, failure behavior, local preparation과 external mutation 사이의 boundary 정의
- Decision record needed: canonical ownership과 cross-repository authority가 장기적으로 유지되고 rejected alternative가 중요하므로 yes
- Non-goals: 관련 없는 integration 재설계, 모든 adapter detail에 decision record 요구

### 수정된 finish gate

- Requirement reference가 더 좁은 authority requirement를 가리킴
- Test가 authorized success, denied authority, duplicate request, external failure를 cover함
- Implementation과 behavior spec이 해당 requirement와 일치함
- Decision record가 canonical ownership, delegated authority, rejected alternative를 보존함
- Structural check와 project가 선택한 validation check가 통과함

### 리뷰 초점

Reviewer는 나중에 추가한 requirement와 decision record를 implementation-first sequence가 완전한 RDD였다는 증거로 설명하면 안 됩니다. Correction은 durable trace를 복구합니다. Adoption gate는 다음 high-impact implementation을 시작하기 전에 그 trace를 사용할 수 있게 하기 위해 존재합니다.
