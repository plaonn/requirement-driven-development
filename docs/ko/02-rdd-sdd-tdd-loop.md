# RDD, SDD, TDD

RDD, SDD, TDD는 같은 개발 루프의 서로 다른 계층에서 동작합니다.

```text
RDD: Requirement Driven Development, 요구사항 주도 개발
SDD: Spec Driven Development, 명세 주도 개발
TDD: Test Driven Development, 테스트 주도 개발
```

셋은 경쟁 관계가 아닙니다. RDD는 requirement를 루프의 최상위에 두고, SDD와 TDD는 더 구체적인 피드백 메커니즘을 제공합니다.

## 계층 모델

```text
Requirement
  -> Spec
    -> Test
      -> Implementation
```

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

## TDD: 실행 가능한 피드백으로서의 test

TDD는 묻습니다.

```text
현재 spec을 실행 가능한 검사로 계속 증명할 수 있는가?
```

Test는 requirement가 아닙니다. Spec에서 파생된 실행 가능한 checkpoint입니다.

## 한 루프 안에서 바뀔 수 있는 것

```text
보통 안정적인 것:
  requirement 의도

진화할 수 있는 것:
  spec 세부사항
  test 예시
  implementation 구조

명시해야 하는 것:
  requirement 변경
```

## 흔한 실패 모드

### 테스트 주도이지만 요구사항 주도는 아닌 경우

Test는 통과하지만 결과가 원래 requirement를 만족하지 못합니다.

### 명세 주도이지만 요구사항 주도는 아닌 경우

Spec은 자세하지만 잘못된 사용자 또는 제품 필요를 인코딩합니다.

### 구현 주도 루프

Implementation이 loop의 목적을 형성하기 시작합니다.

이 경우 유용해 보이는 변경이 requirement와 연결되지 않은 채 loop에 들어오며 숨은 scope creep이 생깁니다.
