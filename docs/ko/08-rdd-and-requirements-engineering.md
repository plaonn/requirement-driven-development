# RDD와 요구공학

요구사항 주도 개발(Requirement Driven Development, RDD)은 요구공학(Requirements Engineering)과 관련이 있지만, 더 넓은 요구공학 분야를 대체하지 않습니다.

## 요구공학의 범위

요구공학은 stakeholder의 필요를 이해하고, 그 필요를 만족하지 못하는 system을 만들 위험을 줄이기 위한 체계적인 작업을 다룹니다. 일반적으로 다음 활동을 포함합니다.

- requirement source와 stakeholder 식별
- candidate requirement 도출
- feasibility, ambiguity, dependency, conflict 분석
- requirement 협상과 우선순위 결정
- functional requirement, quality requirement, constraint 명세
- stakeholder need를 기준으로 requirement 검증
- lifecycle 전체에서 requirement version, change, traceability 관리

이 활동들은 iterative하게 진행될 수 있습니다. 요구공학은 upfront requirement document 작성에만 한정되지 않으며, implementation이 시작됐다고 끝나는 활동도 아닙니다.

## RDD의 범위

RDD는 더 좁은 문제를 다룹니다.

```text
현재 개발 loop의 candidate requirement가 주어졌을 때,
그 requirement에서 direct acceptance evidence와 review까지 loop를 추적 가능하게 유지한다.
```

RDD는 candidate requirement가 현재 loop boundary로 사용될 만큼 충분히 도출되고 검증되었다고 전제합니다. 그 뒤 다음 관계를 연결합니다.

```text
Requirement -> Spec / acceptance -> Implementation -> Test / acceptance evidence -> Review
```

RDD의 주된 관심사는 다음과 같습니다.

- 작은 개발 loop의 목적과 경계 보존
- loop requirement에서 spec과 test 파생
- implementation이 이끄는 scope growth 감지
- requirement 변경 명시
- re-scope, split, follow-up loop 중 적절한 경계 결정
- 최종 변경을 그 변경을 정당화한 requirement까지 추적

## RDD가 대체하지 않는 것

RDD는 다음을 위한 완전한 방법을 제공하지 않습니다.

- 관련 stakeholder 전체 발견
- 알려지지 않았거나 충돌하는 need 도출
- market 또는 product discovery
- stakeholder conflict 해결
- product 또는 portfolio 전체의 requirement prioritization
- system-wide feasibility 분석
- 완전한 requirement baseline 또는 traceability model 유지
- product 전체가 stakeholder와 business need를 만족하는지 검증

이 책임에는 적절한 요구공학, product discovery, domain analysis, safety, security, governance 실천을 사용해야 합니다. RDD는 그 결과를 작은 개발 loop의 candidate requirement로 받을 수 있습니다.

RDD는 loop를 정당화하는 context와 loop를 고정하는 requirement를 구분합니다. 명시적인 `Need`, `Goal`, `Requirement`, `Spec`, `Implementation choice` convention은 [RDD 방법론 — 용어 경계](01-methodology.md#용어-경계)를 참고합니다.

## 두 영역이 만나는 지점

RDD는 요구공학의 여러 관심사를 task, ticket, pull request, 작은 iteration 규모에 적용합니다.

| 요구공학 관심사 | RDD 적용 |
| --- | --- |
| Traceability | Loop requirement를 spec, implementation, 직접적인 acceptance evidence, review에 연결합니다. |
| Change management | Requirement 변경을 명시적인 loop-boundary event로 취급합니다. |
| Scope control | Requirement에서 벗어난 작업을 split, re-scope, defer합니다. |
| Specification | Loop 안에서 rule, contract, boundary, acceptance criteria를 다듬습니다. |
| Verification | Test와 다른 check로 implementation이 현재 spec과 requirement를 만족하는지 보여 주는 evidence를 만듭니다. |
| Validation | Implementation과 evidence에서 requirement로 역추적하고, 변경이 loop를 정당화한 need를 여전히 해결하는지 review합니다. |

RDD trace는 의도적으로 가볍습니다. Lifecycle 전체의 traceability가 필요한 project에서는 requirement source, stakeholder, dependent requirement, architecture, release, 관련 work product의 연결도 별도로 유지해야 합니다.

## RDD loop로 넘기기 전 확인

Candidate requirement를 loop anchor로 사용하기 전에, 경계를 추측으로 만들지 않을 만큼의 맥락을 확인합니다.

```text
Source or stakeholder:
  이 need는 어디에서 왔는가?

Need or root goal:
  어떤 문제, 바람, desired state가 이 loop를 정당화하는가?

Candidate requirement:
  이 loop에서 어떤 capability, quality, constraint 또는 condition이 참이어야 하는가?

Rationale and failure prevented:
  왜 중요하며, 없으면 무엇이 잘못되는가?

Validation evidence:
  왜 이것이 현재 loop에 적절한 requirement인가?

Known conflicts or dependencies:
  어떤 다른 need 또는 constraint가 영향을 주는가?
```

작고 명확한 변경에 긴 intake record가 필요한 것은 아닙니다. Candidate requirement의 source, purpose, conflict, adequacy가 불명확하다면 full RDD trace를 파생하기 전에 그 boundary를 먼저 확인합니다.

## 참고 자료

- [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html)
- [IEEE Computer Society — SWEBOK Guide software requirements topics](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics)
- [IREB — CPRE glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary)
