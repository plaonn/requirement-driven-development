# RDD 리뷰 방법

RDD review는 개발 루프가 requirement에서 implementation까지 추적 가능한 상태인지 확인합니다.

이 체크리스트는 PR, ticket, task, 작은 iteration review에 사용할 수 있습니다.

## 리뷰 체크리스트

### 1. Requirement

- [ ] Driving requirement가 명확한가?
- [ ] 원하는 동작뿐 아니라 작업이 존재하는 이유도 설명하는가?
- [ ] 막으려는 실패, regression, risk가 드러나는가?
- [ ] 성공과 관련 없는 변경을 구분할 수 있을 만큼 구체적인가?
- [ ] PR, task, ticket이 여전히 명시된 requirement와 맞는가?
- [ ] 더 큰 root goal이 있다면, 현재 loop의 좁은 requirement가 그 아래 단계로 명확히 표현됐는가?

### 2. Spec

- [ ] Spec이 requirement를 올바르게 표현하는가?
- [ ] 중요한 규칙, 경계, API 계약, 인수 기준이 보이는가?
- [ ] Edge case가 숨은 가정이 아니라 spec refinement로 다뤄졌는가?

### 3. Tests

- [ ] Test가 의미 있는 규칙을 보호하는가?
- [ ] Test가 우연한 구현 세부사항이 아니라 spec에서 파생됐는가?
- [ ] 중요한 negative case 또는 경계가 포함됐는가?
- [ ] Test가 바뀌었다면 여전히 같은 requirement를 보호하는가?

### 4. Implementation

- [ ] Implementation이 test를 만족하는가?
- [ ] Test뿐 아니라 원래 requirement도 만족하는가?
- [ ] Change가 loop가 요구하는 범위만큼 좁은가?
- [ ] 구현 세부사항이 명시된 spec과 일치하는가?

### 5. Scope

- [ ] 관련 없는 동작이 loop에 들어왔는가?
- [ ] Refactoring이 동작 변경을 만들었는가?
- [ ] 구현 편의가 public contract를 확장했는가?
- [ ] 구현 선택이 rationale 없이 requirement로 승격됐는가?
- [ ] 인접한 fix가 분리됐거나 명시적으로 포함됐는가?

### 6. Automation boundary

사용자, 운영, 금융, safety-sensitive 작업 또는 다른 state-changing work를 자동화하는 loop라면 이 항목을 사용합니다.

- [ ] 지금 자동화해도 되는 일이 명확한가?
- [ ] 준비는 가능하지만 사람 review가 필요한 일이 명확한가?
- [ ] 아직 자동화하지 말아야 할 일이 명확한가?
- [ ] 장기 목표가 더 넓은 자동화라면, 현재 safety stage가 명시됐는가?

### 7. 변경 경계

- [ ] 구현 중 requirement가 바뀌었는가?
- [ ] 바뀌었다면 loop가 명시적으로 re-scope, split, restart됐는가?
- [ ] Requirement 변경이 reviewer에게 보이는 곳에 설명됐는가?

### 8. Non-goals

- [ ] 제외된 항목이 명시되어 있는가?
- [ ] Reviewer가 빠진 일을 실수로 오해하지 않도록 되어 있는가?
- [ ] Follow-up item이 현재 loop와 분리되어 있는가?

## 실제 review 흐름

Diff가 아니라 requirement부터 봅니다.

Requirement의 root goal, rationale, failure prevented, 구현 선택과 requirement의 경계, automation boundary가 불명확하면 full trace를 쓰기 전에 boundary clarification을 합니다. Loop boundary를 정하는 데 필요한 최소 질문을 먼저 하고, 그 뒤 review를 이어갑니다.

그다음 구현 세부사항을 판단하기 전에 spec과 test를 읽습니다. 이렇게 하면 review가 루프 경계에 고정되고, implementation이 조용히 목표를 재정의하는 일을 막을 수 있습니다.
