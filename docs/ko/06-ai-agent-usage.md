# AI coding agent에서의 RDD

AI coding agent는 RDD의 한 적용 영역일 뿐이며, 방법론의 주 목적은 아닙니다.

RDD는 먼저 일반적인 소프트웨어 작업에 적용됩니다: pull request, ticket, task, 작은 iteration. Agent는 구현 흐름을 따라 인접 작업으로 확장되기 쉽기 때문에 같은 구조에서 특히 이점을 얻습니다.

## Agent 루프 경계

Agent에게는 안정적인 requirement, 명시적인 spec, tests, non-goals를 제공해야 합니다.

Agent는 같은 requirement를 계속 표현하는 범위에서만 spec과 test를 refine해야 합니다. Requirement가 바뀌는 것처럼 보이면 scope를 확장하기 전에 멈추고 보고해야 합니다.

## 유용한 agent 지시 구조

```text
Requirement:
  이 task가 만족해야 하는 안정적인 requirement

Spec:
  규칙, 계약, 인수 기준, 경계

Tests:
  Required tests or checks

Non-goals:
  Scope 밖에 있어야 하는 adjacent work

중단 조건:
  계속 진행하지 말고 보고해야 하는 조건
```

## 중단 조건

Agent는 다음 상황에서 멈추거나 보고해야 합니다.

- Requirement가 틀렸거나 불완전해 보일 때
- Implementation이 adjacent feature를 제안하게 만들 때
- Test 변경이 requirement 자체를 바꾸는 방향일 때
- 발견한 bug가 다른 requirement에 속할 때
- Non-goal이 task 완료에 필요해 보일 때
- 요청된 변경이 더 넓은 architecture 또는 API decision을 요구할 때

## Scope 관리

Agent는 implementation 중 adjacent work가 보여도 임의로 scope를 확장하면 안 됩니다.

예시:

- Cancellation task가 order editing으로 바뀌면 안 됩니다.
- Refactoring task가 동작 변경을 숨기면 안 됩니다.
- Bug fix가 명시적 re-scope 없이 related workflow redesign이 되면 안 됩니다.

## Final trace

작업 끝에 agent는 다음 final trace를 요약해야 합니다.

```text
Requirement -> Spec -> Tests -> Implementation
```
