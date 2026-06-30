# RDD Review Method

RDD review는 개발 루프가 requirement에서 implementation까지 추적 가능한 상태인지 확인합니다.

이 checklist는 PR, ticket, task, 작은 iteration review에 사용할 수 있습니다.

## Review checklist

### 1. Requirement

- [ ] Driving requirement가 명확한가?
- [ ] 성공과 관련 없는 변경을 구분할 수 있을 만큼 구체적인가?
- [ ] PR, task, ticket이 여전히 stated requirement와 맞는가?

### 2. Spec

- [ ] Spec이 requirement를 올바르게 표현하는가?
- [ ] 중요한 rules, boundaries, API contracts, acceptance criteria가 보이는가?
- [ ] Edge case가 숨은 가정이 아니라 spec refinement로 다뤄졌는가?

### 3. Tests

- [ ] Test가 의미 있는 rule을 보호하는가?
- [ ] Test가 incidental implementation detail이 아니라 spec에서 파생됐는가?
- [ ] 중요한 negative case 또는 boundary가 포함됐는가?
- [ ] Test가 바뀌었다면 여전히 같은 requirement를 보호하는가?

### 4. Implementation

- [ ] Implementation이 test를 만족하는가?
- [ ] Test뿐 아니라 원래 requirement도 만족하는가?
- [ ] Change가 loop가 요구하는 범위만큼 좁은가?
- [ ] Implementation detail이 stated spec과 일치하는가?

### 5. Scope

- [ ] 관련 없는 behavior가 loop에 들어왔는가?
- [ ] Refactoring이 behavior change를 만들었는가?
- [ ] Implementation convenience가 public contract를 확장했는가?
- [ ] Adjacent fix가 분리됐거나 명시적으로 포함됐는가?

### 6. Change boundary

- [ ] 구현 중 requirement가 바뀌었는가?
- [ ] 바뀌었다면 loop가 명시적으로 re-scope, split, restart됐는가?
- [ ] Requirement change가 reviewer에게 보이는 곳에 설명됐는가?

### 7. Non-goals

- [ ] 제외된 항목이 명시되어 있는가?
- [ ] Reviewer가 빠진 일을 실수로 오해하지 않도록 되어 있는가?
- [ ] Follow-up item이 현재 loop와 분리되어 있는가?

## 실제 review 흐름

Diff가 아니라 requirement부터 봅니다.

그다음 implementation detail을 판단하기 전에 spec과 test를 읽습니다. 이렇게 하면 review가 loop boundary에 고정되고, implementation이 조용히 goal을 재정의하는 일을 막을 수 있습니다.
