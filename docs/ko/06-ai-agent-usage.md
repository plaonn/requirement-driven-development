# AI coding agent에서의 RDD

AI coding agent는 RDD의 한 적용 영역일 뿐이며, 방법론의 주 목적은 아닙니다.

RDD는 먼저 일반적인 소프트웨어 작업에 적용됩니다: pull request, ticket, task, 작은 iteration. Agent는 구현 흐름을 따라 인접 작업으로 확장되기 쉽기 때문에 같은 구조에서 특히 이점을 얻습니다.

## Agent 루프 경계

Agent에게는 안정적인 requirement, 명시적인 spec, acceptance boundary, non-goals를 제공해야 합니다. Agent는 어떤 file이나 test를 건드릴지뿐 아니라 어떤 observable evidence가 requirement를 입증하는지도 식별할 수 있어야 합니다.

Agent는 같은 requirement를 계속 표현하는 범위에서만 spec과 test를 refine해야 합니다. Requirement가 바뀌는 것처럼 보이면 scope를 확장하기 전에 멈추고 보고해야 합니다.

## Lightweight agent trace

작은 agent loop라면 별도 `REQUIREMENTS.md`, active-loop file, heavyweight artifact를 만들 필요가 없습니다. 최소 semantic trace를 task, PR, commit message, agent final review 안에 간결하게 남길 수 있습니다.

```text
Outcome / Goal:
  Desired state

Requirement:
  반드시 참이어야 하는 stable condition

Done when / Acceptance:
  Requirement를 판별할 수 있는 observable evidence
```

이것은 operational label의 예시이지 RDD가 강제하는 schema가 아닙니다. 더 크거나 위험한 loop는 full requirement 문서, validity lifecycle, decision record, 보존할 loop artifact를 사용할 수 있습니다. 작은 loop는 짧은 requirement 한 문장과 evidence 한 줄만으로도 충분할 수 있지만, semantic distinction은 보여야 합니다.

## 유용한 agent 지시 구조

```text
Need / goal context:
  이 task를 정당화하는 stakeholder 문제, 바람 또는 desired outcome

Requirement:
  이 task가 만족해야 하는 안정적인 capability, quality, constraint 또는 condition
  requirement가 loop 이후에도 유지될 수 있다면 rationale, failure prevented, assumptions, revisit 조건을 포함
  더 큰 root goal의 일부라면 현재 좁은 stage를 명시

Requirement validity:
  Loop-local requirement, durable requirement, temporary/scoped policy 중 하나
  Durable requirement에는 assumptions와 observable revisit signal이 필요
  Temporary/scoped policy에는 expiration rule이 필요

Spec:
  규칙, 계약, 인수 기준, 경계

Tests:
  Required tests or checks

Acceptance evidence / Done when:
  Satisfied, unsatisfied, unknown을 구분하는 observable result

Non-goals:
  Scope 밖에 있어야 하는 adjacent work

중단 조건:
  계속 진행하지 말고 보고해야 하는 조건

Automation boundary:
  state-changing work라면 지금 자동화해도 되는 일, human review가 필요한 일, 아직 자동화하지 말아야 할 일을 명시
```

## 중단 조건

Agent는 다음 상황에서 멈추거나 보고해야 합니다.

- root goal, rationale, failure prevented, automation boundary가 불명확해 full trace를 만들려면 추측이 필요할 때
- Prompt에 goal 또는 desired outcome은 있지만 무엇이 참이어야 하는지 말하는 requirement가 없을 때
- Assumption이 깨졌거나 revisit signal이 발생했지만 requirement가 revalidate되지 않았을 때
- Requirement가 틀렸거나 불완전해 보일 때
- Implementation이 adjacent feature를 제안하게 만들 때
- Test 변경이 requirement 자체를 바꾸는 방향일 때
- Requirement에 대한 직접적인 acceptance evidence가 없을 때는 `unknown`으로 보고하고 완료라고 주장하지 않습니다.
- 발견한 bug가 다른 requirement에 속할 때
- Non-goal이 task 완료에 필요해 보일 때
- 요청된 변경이 더 넓은 architecture 또는 API decision을 요구할 때

이 경우 agent는 boundary clarification을 사용해야 합니다. 계속 진행하기 전에 loop boundary를 정하는 데 필요한 최소 질문을 먼저 합니다.

Implementation 또는 test refinement가 항상 boundary change인 것은 아닙니다. Internal architecture, internal API 또는 data structure, test strategy 또는 location, 같은 requirement를 위한 acceptance refinement, bounded refactoring은 loop 안에 남을 수 있습니다. Capability, actor 또는 scope, trigger, obligation, accepted failure mode, user-facing behavior, authority, security/privacy boundary, public contract가 materially 바뀌면 re-scope해야 합니다.

Revisit signal이 발생한 뒤 agent는 requirement를 조용히 계속 사용하면 안 됩니다. Evidence를 보고하고 `retain`, `narrow`, `supersede`, `discard` decision을 요청하거나 복원하며, 영향받는 spec, test, implementation, docs, active loop를 식별해야 합니다.

## Scope 관리

Agent는 implementation 중 adjacent work가 보여도 임의로 scope를 확장하면 안 됩니다.

Test 통과, commit, task 완료는 required condition에 대한 직접적인 evidence를 제공할 때만 requirement satisfaction의 근거가 됩니다. Evidence가 satisfaction과 non-satisfaction을 구분하지 못하면 loop를 닫지 말고 `unknown`으로 보고합니다.

예시:

- Cancellation task가 order editing으로 바뀌면 안 됩니다.
- Refactoring task가 동작 변경을 숨기면 안 됩니다.
- Bug fix가 명시적 re-scope 없이 related workflow redesign이 되면 안 됩니다.

## Final trace

작업 끝에 agent는 다음 final trace를 요약해야 합니다.

```text
Requirement -> Spec / acceptance -> Tests/Checks -> Implementation / evidence

Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```

PR이 없는 workflow에서는 이 final trace가 task 또는 change set의 review surface 역할도 할 수 있습니다. 자주 읽을 수 있을 만큼 compact해야 하지만, agent가 requirement를 바꿨는지, spec을 refine했는지, local implementation progress를 원래 requirement까지 역추적했는지, 다른 loop로 넘길 follow-up을 발견했는지는 드러나야 합니다. 역방향은 agent-specific runtime protocol이나 mandatory tool call이 아니라 review guidance입니다.
