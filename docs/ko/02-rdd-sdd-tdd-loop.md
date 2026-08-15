# RDD, SDD, TDD

RDD, SDD, TDD는 같은 개발 루프의 서로 다른 계층에서 동작합니다.

```text
RDD: Requirement Driven Development, 요구사항 주도 개발
SDD: Spec Driven Development, 명세 주도 개발
TDD: Test Driven Development, 테스트 주도 개발
```

셋은 경쟁 관계가 아닙니다. RDD는 accepted loop requirement를 development trace의 최상위에 두고, SDD와 TDD는 더 구체적인 피드백 메커니즘을 제공합니다. Requirement를 정당화하는 need 또는 goal은 또 하나의 implementation layer가 아니라 연결된 context로 유지합니다.

## 계층 모델

```text
Need / goal context
  -> Accepted loop requirement
  -> Spec / acceptance definition
  -> Implementation
  -> Test / acceptance evidence
```

이것은 반드시 따라야 하는 실행 순서가 아니라 semantic map입니다. Test는 implementation 전에 설계할 수 있고, acceptance evidence는 test, manual check, 문서 review 또는 requirement와 직접 관련된 다른 관찰에서 나올 수 있습니다. 각 계층은 서로 다른 질문에 답합니다.

## RDD: 루프 기준점으로서의 requirement

RDD는 묻습니다.

```text
우리는 여전히 올바른 요구사항을 해결하고 있는가?
```

Requirement는 루프의 기준점입니다. 현재 루프 안에서는 안정적이어야 합니다.

Requirement가 바뀌면 루프는 명시적으로 re-scope되어야 합니다.

## SDD: 계약으로서의 spec

SDD는 묻습니다.

```text
요구사항을 명확한 동작, 규칙, 경계로 표현했는가?
```

Spec은 루프 안에서 진화할 수 있습니다. 구현과 리뷰를 거치며 edge case, 빠진 제약, 더 나은 표현을 발견하기 때문입니다.

Spec refinement가 반드시 requirement 변경을 뜻하지는 않습니다.

예시:

```text
Requirement:
  사용자는 fulfillment가 시작되기 전에 주문을 취소할 수 있다.

Spec refinements:
  - 결제된 주문은 refund flow를 시작한다.
  - Fulfillment 중인 주문은 취소할 수 없다.
  - 복원된 coupon은 원래 validity window를 넘지 않아야 한다.
```

Requirement는 안정적으로 유지되고, spec은 더 정교해집니다.

## TDD: 실행 가능한 피드백으로서의 test

TDD는 묻습니다.

```text
현재 spec을 실행 가능한 검사로 계속 증명할 수 있는가?
```

Test는 requirement가 아닙니다. Spec에서 파생된 실행 가능한 checkpoint입니다.

Test 통과가 requirement evidence를 갖췄다는 뜻은 아닙니다. Evidence는 requirement와 직접 관련되고 `satisfied`, `unsatisfied`, `unknown`을 구분할 수 있어야 합니다. Unknown은 satisfied가 아닙니다.

Test는 다음과 같은 경우 바뀔 수 있습니다.

- spec이 더 정확해질 때
- edge case가 발견될 때
- test가 과도하게 세부 구현을 고정했을 때
- behavior는 유지하면서 implementation design이 바뀔 때
- 더 나은 example이 같은 rule을 명확하게 표현할 때

## 한 루프 안에서 바뀔 수 있는 것

```text
보통 안정적인 것:
  requirement 의도

진화할 수 있는 것:
  Internal architecture
  Internal API와 data structure
  spec 세부사항
  test 예시
  Test strategy 또는 location
  같은 requirement를 검증하도록 다듬은 acceptance criteria
  implementation 구조
  Bounded refactoring

명시해야 하는 것:
  requirement 변경
```

## 흔한 실패 모드

### 테스트 주도이지만 요구사항 주도는 아닌 경우

Test는 통과하지만 결과가 원래 requirement를 만족하지 못합니다.

Test가 불완전한 spec 해석을 기준으로 작성됐을 때 이런 문제가 자주 생깁니다.

### 명세 주도이지만 요구사항 주도는 아닌 경우

Spec은 자세하지만 잘못된 사용자 또는 제품 필요를 인코딩합니다.

Specification 작업이 원래 requirement에서 분리됐을 때 이런 문제가 자주 생깁니다.

### 구현 주도 루프

Implementation이 loop의 목적을 형성하기 시작합니다.

이 경우 유용해 보이는 변경이 requirement와 연결되지 않은 채 loop에 들어오며 숨은 scope creep이 생깁니다.

### Delivery는 완료됐지만 requirement가 입증되지 않은 경우

Implementation이 merge되고 test가 통과하고 task가 완료 처리되어도 직접적인 requirement evidence가 없을 수 있습니다. 이때 requirement 상태는 satisfied가 아니라 `unknown`입니다. Review는 delivery hygiene를 acceptance로 간주하지 말고 requirement로 돌아가야 합니다.

## RDD의 실용적 입장

RDD는 spec과 test가 덜 중요하다고 말하지 않습니다.

Spec과 test가 loop를 정의하는 requirement까지 계속 추적 가능해야 한다고 말합니다.

따라서 review 방향은 다음과 같습니다.

```text
Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```
