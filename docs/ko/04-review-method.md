# RDD 리뷰 방법

RDD review는 개발 루프가 requirement에서 implementation을 거쳐 직접적인 acceptance evidence까지 추적 가능한지 확인합니다.

이 체크리스트는 PR, ticket, task, 작은 iteration review에 사용할 수 있습니다.

## 리뷰 체크리스트

### 1. Requirement

- [ ] Loop를 정당화하는 stakeholder need 또는 root goal이 명확한가?
- [ ] Driving requirement가 명확한가?
- [ ] Requirement가 반드시 만족해야 하는 capability, quality, constraint 또는 condition을 말하는가?
- [ ] Internal architecture, API, data structure, spec, test strategy가 바뀌어도 stable한가?
- [ ] Loop를 완료했다고 하기 위해 반드시 참이어야 하는 normative condition인가?
- [ ] Evidence가 satisfied, unsatisfied, unknown을 구분할 수 있을 만큼 discriminating한가?
- [ ] Filename, internal API, command, test location 같은 solution detail이 아닌 solution-independent한가?
- [ ] 여러 의무가 들어 있다면 소수의 atomic requirement로 나눌 필요가 없는가?
- [ ] 연결된 need, goal, rationale이 작업이 존재하는 이유를 설명하는가?
- [ ] 막으려는 실패, regression, risk가 드러나는가?
- [ ] 성공과 관련 없는 변경을 구분할 수 있을 만큼 구체적인가?
- [ ] PR, task, ticket이 여전히 명시된 requirement와 맞는가?
- [ ] 더 큰 root goal이 있다면, 현재 loop의 좁은 requirement가 그 아래 단계로 명확히 표현됐는가?

### 2. Requirement validity

- [ ] 이 항목이 loop-local requirement, durable requirement, temporary/scoped policy 중 무엇인지 명시됐는가?
- [ ] Durable이라면 assumptions와 observable `Revisit when` signal이 명시됐는가?
- [ ] Temporary 또는 scoped policy라면 expiration rule이 명시됐는가?
- [ ] Assumption이 깨졌거나 revisit signal이 발생했는가?
- [ ] Revalidation을 했다면 결과가 `retain`, `narrow`, `supersede`, `discard` 중 하나로 명시됐는가?
- [ ] 영향받는 spec, test, implementation, docs, active loop가 갱신되거나 중단됐는가?

### 3. Spec

- [ ] Spec이 requirement를 올바르게 표현하는가?
- [ ] 중요한 규칙, 경계, API 계약, 인수 기준이 보이는가?
- [ ] Edge case가 숨은 가정이 아니라 spec refinement로 다뤄졌는가?

### 4. Tests와 acceptance evidence

- [ ] Test가 의미 있는 규칙을 보호하는가?
- [ ] Test가 우연한 구현 세부사항이 아니라 spec에서 파생됐는가?
- [ ] 중요한 negative case 또는 경계가 포함됐는가?
- [ ] Test가 바뀌었다면 여전히 같은 requirement를 보호하는가?
- [ ] Implementation detail이 아니라 requirement에 직접 관련된 observable acceptance evidence가 있는가?
- [ ] Evidence가 `satisfied`, `unsatisfied`, `unknown`을 구분할 수 있는가?
- [ ] `unknown`을 `satisfied`와 분리했는가?
- [ ] Test 통과, commit 생성, task 완료를 required condition을 직접 관찰한 경우가 아니면 requirement satisfaction과 분리했는가?

### 5. Implementation

- [ ] Implementation이 test를 만족하는가?
- [ ] Test뿐 아니라 원래 requirement도 만족하는가?
- [ ] Change가 loop가 요구하는 범위만큼 좁은가?
- [ ] 구현 세부사항이 명시된 spec과 일치하는가?
- [ ] Implementation progress와 acceptance evidence를 분리했는가?

### 6. Scope

- [ ] 관련 없는 동작이 loop에 들어왔는가?
- [ ] Refactoring이 동작 변경을 만들었는가?
- [ ] 구현 편의가 public contract를 확장했는가?
- [ ] 구현 선택이 rationale 없이 requirement로 승격됐는가?
- [ ] 같은 requirement의 refinement(internal architecture, API, data structure, test strategy/location, acceptance refinement, bounded refactor)와 material requirement 변경을 구분했는가?
- [ ] Capability, actor/scope, trigger, obligation, failure mode, user-facing behavior, authority, security/privacy boundary, public contract가 바뀌었다면 loop를 re-scope했는가?
- [ ] Temporary experiment policy나 provider workaround가 promotion rule 없이 durable requirement로 승격됐는가?
- [ ] Decision이 accepted라면 acceptance scope가 명시됐는가?
- [ ] 인접한 fix가 분리됐거나 명시적으로 포함됐는가?

### 7. Automation boundary

사용자, 운영, 금융, safety-sensitive 작업 또는 다른 state-changing work를 자동화하는 loop라면 이 항목을 사용합니다.

- [ ] 지금 자동화해도 되는 일이 명확한가?
- [ ] 준비는 가능하지만 사람 review가 필요한 일이 명확한가?
- [ ] 아직 자동화하지 말아야 할 일이 명확한가?
- [ ] 장기 목표가 더 넓은 자동화라면, 현재 safety stage가 명시됐는가?

### 8. 변경 경계

- [ ] 구현 중 requirement가 바뀌었는가?
- [ ] 바뀌었다면 loop가 명시적으로 re-scope, split, restart됐는가?
- [ ] Requirement 변경이 reviewer에게 보이는 곳에 설명됐는가?

### 9. Non-goals

- [ ] 제외된 항목이 명시되어 있는가?
- [ ] Reviewer가 빠진 일을 실수로 오해하지 않도록 되어 있는가?
- [ ] Follow-up item이 현재 loop와 분리되어 있는가?

### 10. 위험 기반 adoption evidence

Loop가 [기존 프로젝트 forward adoption gate](07-retroactive-rdd-review.md#위험-기반-forward-adoption-gate)를 trigger한 경우 이 section을 사용합니다.

- [ ] 구현 전에 관련 requirement source를 읽었는가?
- [ ] Broad root goal에만 의존하지 않고 구체적인 requirement가 capability와 authority 또는 failure boundary를 cover하는가?
- [ ] Canonical ownership, trust boundary, delegated authority, rejected alternative decision이 장기 가치가 있을 때 보존되는가?
- [ ] Requirement coverage, derived behavior spec, tests/checks, implementation, validation evidence가 모두 보이는가?
- [ ] 이 risk level에 대해 프로젝트가 선택한 local 또는 CI check를 실행했는가?

## 실제 review 흐름

Diff가 아니라 requirement와 validity condition부터 봅니다.

Requirement의 root goal, rationale, failure prevented, decision class, 구현 선택과 requirement의 경계, automation boundary가 불명확하면 full trace를 쓰기 전에 boundary clarification을 합니다. Loop boundary를 정하는 데 필요한 최소 질문을 먼저 하고, 그 뒤 review를 이어갑니다.

그다음 구현 세부사항을 판단하기 전에 spec과 test를 읽습니다. 직접적인 acceptance evidence도 별도로 확인합니다. 이렇게 하면 review가 루프 경계에 고정되고, implementation이나 delivery hygiene가 조용히 목표를 재정의하거나 acceptance를 대신하는 일을 막을 수 있습니다.

마지막에는 다음처럼 정방향뿐 아니라 역방향으로도 review합니다.

```text
Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```

직접적인 evidence가 없으면 requirement 상태는 `unknown`입니다. Test 통과, commit, task 완료를 증거로 취급해 loop를 닫지 않습니다.

마지막으로 assumption이 깨졌는지, revisit signal이 발생했는지, implementation 중 발견한 내용이 requirement를 바꿨는지 확인합니다. 해당한다면 requirement를 revalidate하고 그 결과를 단순 code review comment가 아니라 boundary decision으로 다룹니다.

Risk-sensitive adoption loop에서는 test 통과와 behavior spec 갱신이 필요하지만 그것만으로 finish gate가 완성되지는 않습니다. 완료 전에 durable requirement coverage와 필요한 decision record를 확인합니다.
