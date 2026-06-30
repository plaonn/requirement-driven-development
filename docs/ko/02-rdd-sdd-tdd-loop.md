# RDD, SDD, TDD

RDD, SDD, TDD는 같은 개발 루프의 서로 다른 계층에서 동작합니다.

```text
RDD: Requirement Driven Development
SDD: Spec Driven Development
TDD: Test Driven Development
```

셋은 경쟁 관계가 아닙니다. RDD는 requirement를 루프의 최상위에 두고, SDD와 TDD는 더 구체적인 feedback mechanism을 제공합니다.

## 계층 모델

```text
Requirement
  -> Spec
    -> Test
      -> Implementation
```

## RDD: 루프 anchor로서의 requirement

RDD는 묻습니다.

```text
Are we still solving the right requirement?
```

Requirement는 loop anchor입니다. 현재 루프 안에서는 안정적이어야 합니다.

Requirement가 바뀌면 루프는 명시적으로 재범위화되어야 합니다.

## SDD: 계약으로서의 spec

SDD는 묻습니다.

```text
Have we expressed the requirement as clear behavior, rules, and boundaries?
```

Spec은 루프 안에서 진화할 수 있습니다. 구현과 리뷰를 거치며 edge case, 빠진 제약, 더 나은 표현을 발견하기 때문입니다.

Spec refinement가 반드시 requirement change를 뜻하지는 않습니다.

## TDD: 실행 가능한 feedback으로서의 test

TDD는 묻습니다.

```text
Can the current spec be proven continuously by executable checks?
```

Test는 requirement가 아닙니다. Spec에서 파생된 실행 가능한 checkpoint입니다.

## 한 루프 안에서 바뀔 수 있는 것

```text
Usually stable:
  requirement intent

Expected to evolve:
  spec details
  test examples
  implementation structure

Must be explicit:
  requirement change
```

## 흔한 실패 모드

### Test-driven but not requirement-driven

Test는 통과하지만 결과가 원래 requirement를 만족하지 못합니다.

### Spec-driven but not requirement-driven

Spec은 자세하지만 잘못된 사용자 또는 제품 필요를 encoding합니다.

### Implementation-driven loop

Implementation이 PR의 목적을 형성하기 시작합니다.

이 경우 유용해 보이는 변경이 requirement와 연결되지 않은 채 PR에 들어오며 hidden scope creep이 생깁니다.
