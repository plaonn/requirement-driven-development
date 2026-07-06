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

#### Decision class

RDD는 모든 decision을 지속 requirement로 취급하지 않습니다.

Rule, limit, workaround, review condition을 기록해야 하지만 durable requirement set으로 승격할지 불확실하다면 decision class를 사용합니다.

```text
Durable Requirement:
  앞으로의 loop도 계속 이끌어야 하는 제품, 시스템, safety, 비즈니스, 기술적 필요

Temporary Experiment Policy:
  beta, live test, 시험 금액, 시장, 기간, operator run, 제한된 experiment에만 적용되는 규칙

Provider Workaround:
  특정 provider, platform, API, app check, 외부 dependency 동작 때문에 생긴 제약

Implementation Choice:
  requirement를 만족하기 위해 현재 선택한 설계나 코드 구조. 그 자체가 requirement는 아님

Promotion Candidate:
  evidence가 쌓이면 durable requirement가 될 수 있는 반복 policy 또는 workaround

Expired/Superseded Policy:
  새 작업을 이끌면 안 되고 historical context로만 남는 policy
```

`accepted`라는 말에는 항상 scope가 붙어야 합니다.

```text
Acceptance scope:
  system-wide requirement accepted
  beta-only policy accepted
  operator-run-specific risk accepted
  code-unlock condition accepted but implementation blocked
```

Policy나 decision record에는 다음 필드가 유용합니다.

```text
Decision class:
Durability:
Acceptance scope:
Policy horizon:
Promotion rule:
Expiration rule:
Canonical owner:
```

Decision이 여러 experiment에 반복 적용되고, 위반 시 금융/보안/safety/external side effect 위험이 크고, provider가 바뀌어도 유지될 원칙이며, 여러 implementation surface에 영향을 주고, operator flow와 test가 함께 따라야 한다면 requirement 승격 후보가 됩니다.

특정 종목, 금액, 시장, provider check 결과, beta run, 기간, 한두 번의 experiment에만 적용된다면 durable requirement보다 policy로 남기는 편이 맞습니다. Temporary policy도 유효한 RDD artifact입니다. 문제는 promotion 또는 expiration rule 없이 영구 system requirement처럼 읽히는 것입니다.

#### Boundary clarification

때로 가장 유용한 RDD 단계는 full trace를 쓰는 것이 아니라, 먼저 멈춰서 loop boundary를 확인하는 것입니다.

다음이 불명확하면 spec, test, implementation을 파생하기 전에 boundary clarification을 합니다.

- loop가 기여하는 root goal
- requirement가 막으려는 rationale 또는 failure
- 어떤 제약이 지속 requirement, temporary policy, provider workaround, implementation choice인지
- state-changing work의 automation boundary
- 더 큰 장기 goal 아래의 현재 safety stage

이 경우 candidate requirement를 confirm, reject, narrow, supersede하는 데 필요한 최소 질문을 먼저 합니다. 빈 rationale을 추측으로 채우지 않습니다. Boundary가 명확해진 뒤 일반 RDD trace를 이어갑니다.

#### 루프 requirement와 지속 requirement

개발 루프를 정의하는 requirement는 그 루프의 경계이지만, 루프가 끝났다고 반드시 사라져야 하는 것은 아닙니다.

어떤 requirement는 단일 task context로 끝납니다. 반면 어떤 requirement는 이후 설계 변경을 계속 이끄는 제품 또는 시스템 requirement로 남아야 합니다. 루프 밖에서도 유효하게 남길 requirement라면, 그 제약이 왜 존재하는지 판단할 수 있을 만큼의 맥락을 보존해야 합니다.

오래 살아야 하는 requirement에는 다음 필드가 유용합니다.

```text
Decision class:
  Durable Requirement.

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

#### Requirement 문서 구조

프로젝트가 지속 requirement를 source-of-truth 문서로 유지한다면, entry point는 빠르게 훑을 수 있어야 합니다. 최상위 `REQUIREMENTS.md`는 root goal, requirement hierarchy, 세부 문서 링크를 담는 역할을 할 수 있습니다.

특정 requirement가 자체 rationale, assumptions, derived specs, tests, decisions, revisit history를 가질 만큼 커지면, 그 세부 내용은 `docs/requirements/R1-project-navigation.md` 같은 더 좁은 문서로 분리하는 편을 선호합니다. Index 문서는 긴 논의 archive가 아니라 현재 truth map으로 유지합니다.

분리 기준은 단순 파일 길이가 아닙니다. 사람이나 agent가 task를 수행할 때 필요한 context loading unit과 문서 단위가 어긋날 때 분리합니다. Active contract를 이해하려면 항상 함께 읽어야 하는 requirement set이라면 불필요하게 나누지 않습니다.

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
