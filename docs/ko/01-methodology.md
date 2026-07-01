# RDD 방법론

요구사항 주도 개발(RDD)은 작은 개발 루프를 그 루프를 이끄는 requirement와 정렬된 상태로 유지하기 위한 가벼운 방법론입니다.

RDD의 기본 주장은 단순합니다.

```text
개발 루프는 requirement, spec, test, implementation, review가 서로 추적 가능할 때 건강하다.
```

## 용어 원칙

이 문서는 한국어 독자를 위한 companion 문서이지만, software development에서 널리 쓰이는 영어 용어는 일부 유지합니다.

- requirement: 요구사항
- spec: 명세 또는 규칙
- test: 테스트 또는 실행 가능한 검사
- implementation: 구현
- review: 리뷰
- loop boundary: 루프 경계

## 개발 루프

개발 루프는 pull request, task, ticket, story, bug fix, 작은 agile iteration일 수 있습니다.

RDD는 의도적으로 작은 루프를 대상으로 합니다. Product discovery, roadmap planning, Scrum, Kanban, XP, TDD를 대체하지 않습니다. 그런 실천 위에 일상 개발 작업을 위한 추적 가능성 모델을 제공합니다.

## 루프 경계

RDD에서 모든 루프에는 안정적인 requirement가 필요합니다.

그 requirement가 루프의 경계를 정의합니다.

```text
루프 안:
  spec refinement
  예시 추가
  test 추가
  implementation 단순화
  인수 기준 명확화

루프 밖:
  underlying requirement 변경
  다른 사용자 필요로 목표 확장
  관련 없는 fix 혼합
  opportunistic behavior change 추가
```

Requirement는 틀릴 수 있고, 불완전할 수 있고, 학습 이후 바뀔 수 있습니다.

RDD는 그 가능성을 부정하지 않습니다. 다만 requirement가 바뀌면 루프 경계도 바뀐 것이므로, 그 변경을 명시해야 한다고 봅니다.

## 각 계층의 역할

### Requirement

Requirement는 작업이 존재하는 이유를 설명합니다.

좋은 requirement가 항상 길 필요는 없지만, 성공과 관련 없는 변경을 구분할 수 있을 만큼은 명확해야 합니다.

#### 목적을 보존하는 requirement

Requirement는 원하는 동작만이 아니라 목적도 보존해야 합니다. 목적이 빠지면 구현 선택이 지속 requirement처럼 굳어지기 쉽습니다.

한 번의 작은 변경을 넘어 계속 판단 기준이 될 수 있는 requirement라면 다음을 확인합니다.

```text
Root goal:
  이 loop가 기여하는 더 큰 사용자, 제품, 비즈니스, 운영 목적

Requirement:
  이 loop 안에서 계속 참이어야 하는 것

Rationale:
  이 requirement가 지금 중요한 이유

Failure prevented:
  이 requirement가 막는 나쁜 결과, regression, risk

Assumptions:
  requirement가 유효하려면 참이어야 하는 조건

Revisit when:
  requirement를 narrow, supersede, discard해야 할 미래 신호
```

Root goal은 장기 방향을 한 번에 안전하게 구현할 수 없는 프로젝트에서 특히 유용합니다. 예를 들어 장기 목적은 자동화일 수 있지만, 현재 loop에서는 read-only analysis나 approval-gated execution만 허용할 수 있습니다. RDD는 이것을 충돌로 보지 않고 staged requirement로 표현해야 합니다.

자동화가 중요한 loop에서는 automation boundary도 함께 적습니다.

```text
Automate now:
  추가 review 없이 시스템이 수행해도 되는 일

Require review:
  시스템이 준비할 수 있지만 명시적 사람 승인이 필요한 일

Do not automate yet:
  나중 requirement가 확인될 때까지 scope 밖에 두는 인접 작업
```

#### 루프 requirement와 지속 requirement

개발 루프를 정의하는 requirement는 그 루프의 경계이지만, 루프가 끝났다고 반드시 사라져야 하는 것은 아닙니다.

어떤 requirement는 단일 task context로 끝납니다. 반면 어떤 requirement는 이후 설계 변경을 계속 이끄는 제품 또는 시스템 requirement로 남아야 합니다. 루프 밖에서도 유효하게 남길 requirement라면, 그 제약이 왜 존재하는지 판단할 수 있을 만큼의 맥락을 보존해야 합니다.

오래 살아야 하는 requirement에는 다음 필드가 유용합니다.

```text
Requirement:
  계속 참이어야 하는 사용자, 제품, 비즈니스, 기술적 필요

Rationale:
  그 필요가 중요한 이유

Failure prevented:
  derived spec이 제거되거나 약해졌을 때 생길 문제

Assumptions:
  requirement가 유효한 조건

Derived specs:
  requirement를 만족하기 위해 현재 선택한 규칙 또는 계약

Revisit when:
  requirement를 다시 검토해야 하는 조건
```

목표는 requirement를 긴 설명문으로 만드는 것이 아닙니다. 미래의 maintainer가 어떤 spec은 active requirement를 보호하기 때문에 조심해야 하고, 어떤 spec은 구현 선택이라 바꿀 수 있는지 판단할 수 있을 만큼 intent를 남기는 것입니다.

지속 requirement set은 단순 누적물이 아니라 정리된 현재 truth여야 합니다. 새 requirement가 기존 requirement와 충돌하면 둘을 조용히 공존시키지 말고 supersede, narrow, reject, re-scope 같은 결정을 명시해야 합니다.

### Spec

Spec은 requirement를 규칙, 계약, 경계, 인수 기준으로 옮깁니다.

팀이 requirement를 더 잘 이해하면서 spec은 루프 안에서 진화할 수 있습니다.

### Test

Test는 spec의 일부를 실행 가능하게 만듭니다.

Test는 requirement 자체가 아닙니다. 현재 spec 해석을 보호하는 장치입니다.

### Implementation

Implementation은 test와 원래 requirement를 만족합니다.

Test 통과는 필요조건이지만 충분조건은 아닙니다. Implementation이 requirement 의도를 어기거나 루프 경계를 확장하면 RDD 관점에서는 문제가 있습니다.

### Review

Review는 전체 trace를 확인합니다.

```text
Requirement -> Spec -> Test -> Implementation
```

좋은 review는 code가 동작하는지만 보지 않고, 그 작업이 여전히 현재 루프에 속하는지도 확인합니다.

## 핵심 규칙

```text
Spec/test refinement는 루프 안에서 일어날 수 있다.
Requirement가 바뀌면 루프 경계 변경으로 명시해야 한다.
```
