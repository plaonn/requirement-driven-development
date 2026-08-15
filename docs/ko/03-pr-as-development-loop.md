# 개발 루프로서의 PR

RDD에서 pull request는 단순한 코드 변경 묶음이 아닙니다. PR은 다음 흐름을 가진 작은 개발 루프입니다.

```text
Need / Goal -> Requirement -> Spec -> Implementation -> Test / Acceptance Evidence -> Review
```

이것은 review를 위한 semantic trace이지 반드시 따라야 하는 실행 순서는 아닙니다. Test는 implementation 전에 설계할 수 있고, evidence는 requirement와 직접 관련된 observable check에서 나올 수 있습니다.

## 하나의 안정적인 목적

PR은 하나의 coherent한 need 또는 goal context에 연결된 하나의 안정적인 loop requirement를 가져야 합니다. 그 requirement는 기능, 버그 수정, refactoring, migration, 문서 변경, 운영 개선을 다룰 수 있습니다.

핵심은 PR이 아주 작아야 한다는 뜻이 아닙니다. Reviewer가 어떤 requirement가 루프 경계를 정의하는지 알 수 있어야 한다는 뜻입니다.

## PR 추적 가능성

좋은 PR 설명은 의도에서 code까지의 경로를 드러냅니다.

```text
Need / goal context:
  어떤 stakeholder 문제, 바람, desired outcome이 이 loop를 정당화하는가?

Requirement:
  이 PR이 만족해야 하는 capability, quality, constraint 또는 condition

Spec:
  requirement를 표현하는 규칙, 계약, 경계, 인수 기준

Tests:
  그 규칙을 보호하는 검사

Implementation:
  tests와 requirement를 만족하기 위해 바뀐 것

Non-goals:
  의도적으로 제외한 범위

발견된 requirement 변경:
  구현이나 리뷰 중 원래 requirement 변경 필요가 드러났는가?
```

## PR이 없을 때

RDD는 pull request를 반드시 요구하지 않습니다. 개인 프로젝트, local-only repository, agent-driven workflow에서는 같은 구조를 task, change set, 작은 iteration 규모에 적용할 수 있습니다.

```text
Requirement -> Spec / acceptance -> Implementation -> Checks / evidence -> Review -> Record
```

이 흐름에서는 PR 설명을 task note, agent final trace, commit message body, local change log 같은 다른 review surface가 대신합니다. 하나의 loop는 commit 하나, 여러 commit, 또는 마지막 squash commit으로 남을 수 있습니다. 핵심은 변경을 완료된 것으로 취급하기 전에 loop boundary 결정이 보이게 남는 것입니다.

작은 leaf loop라면 별도 `REQUIREMENTS.md`, active-loop file, heavyweight artifact를 만들 필요가 없습니다. 기존 PR, task, commit 또는 agent review surface에 requirement와 직접적인 acceptance evidence가 보이는 간결한 기록을 남기면 충분합니다. 더 크거나 추상화 수준이 높은 work에는 durable requirement 문서, decision record 또는 더 완전한 loop artifact가 필요할 수 있습니다.

PR 없는 loop에서 유용한 trace는 다음과 같습니다.

```text
Need / goal context:
  어떤 stakeholder 문제, 바람, desired outcome이 이 loop를 정당화하는가?

Requirement:
  이 loop가 만족해야 하는 stable normative condition

Spec / acceptance:
  Requirement를 표현하는 규칙, 경계, observable acceptance condition

Checks / evidence:
  Requirement가 satisfied인지 직접 보여 주는 tests, build, manual check, 문서 review

Implementation:
  바뀐 것

Non-goals:
  의도적으로 제외한 관련 작업

Follow-ups:
  이후 loop로 넘길 발견
```

Trace가 항상 길 필요는 없고, 모든 commit에 들어갈 필요도 없습니다. 작고 명확한 변경은 가볍게 유지할 수 있습니다. 다만 requirement, boundary, 미래 설계 영향이 나중에 재구성되기 어려운 경우에는 trace를 남기는 편이 좋습니다. 직접적인 evidence가 없으면 requirement 상태를 `unknown`으로 기록해야 합니다. Implementation progress, 그것을 cover하지 않는 test 통과, commit 생성, task 완료만으로 satisfied라고 추론하지 않습니다.

## Loop record 보존

RDD는 loop record에 하나의 retention policy를 강제하지 않습니다. 프로젝트는 다음 pattern 중 하나를 선택할 수 있습니다.

- **Persistent record** - 완료된 loop trace를 계속 보존함
- **Disposable active loop** - loop 파일이 있으면 active work로 취급하고, 살아남을 truth를 승격한 뒤 review가 끝나면 loop 파일을 삭제함
- **Selective retention** - audit, safety, 장기 decision 가치가 있는 record만 보존함

세 pattern 모두 같은 completion invariant를 지킵니다. 완료 전에 requirement boundary와 직접적인 requirement-to-evidence trace를 review할 수 있어야 하고, loop 이후에도 살아야 할 정보는 적절한 current-truth surface로 옮겨야 합니다. Durable need와 requirement는 requirement document로, current contract는 docs와 test로, implementation behavior는 code로, 장기 architecture decision은 필요할 때 decision document로 승격합니다. 계속 보존할 가치가 없는 loop-local note는 disposable loop와 함께 사라질 수 있습니다.

Disposable loop 파일은 active working surface이며 필수 archive가 아닙니다. 한 loop는 보통 하나의 pull request, task, ticket, local change set 같은 loop unit을 다뤄야 합니다. 하나의 durable requirement가 여러 loop unit에 걸치면 unit마다 별도 loop record를 만들고 같은 durable requirement를 참조합니다. Structural tooling은 설정된 active-loop directory의 loop 파일을 active work로 취급할 수 있지만 semantic correctness, checkbox 완료 여부, truth promotion 완료 여부를 추론하면 안 됩니다. Filename convention은 RDD invariant가 아니라 project policy로 남습니다.

## 권장 PR 구조

Reviewer가 명시적인 context를 필요로 할 만큼 PR이 크다면 다음 구조를 사용합니다.

```text
# Need / goal context

# Requirement

# Spec

# Tests / acceptance evidence

# Implementation

# Non-goals

# Requirement changes discovered

# Review focus
```

목표는 형식을 늘리는 것이 아니라 scope와 traceability를 review할 수 있게 만드는 것입니다.

## Scope creep 감지

Scope creep은 requirement와 연결되지 않은 유용해 보이는 작업으로 나타나는 경우가 많습니다.

Reviewer는 다음을 확인해야 합니다.

- 관련 없는 동작 변경
- 동작 변경을 숨긴 refactoring
- 구현 중 발견된 bug fix가 같은 PR에 섞인 경우
- 명시된 requirement 밖의 동작을 보호하는 test
- Delivery signal을 직접적인 requirement evidence로 잘못 취급하는 경우
- spec에 없는 API 동작 확장
- 구현보다 넓은 문서 주장

이런 일이 생기면 requirement가 바뀐 것인지, 아니면 추가 작업을 follow-up loop로 옮겨야 하는지 결정해야 합니다.

## Split, re-scope, follow up

작업이 원래 requirement에 더 이상 맞지 않으면 다음 중 하나를 선택합니다.

- **Split** - 서로 독립적으로 review 가능한 requirement일 때
- **Re-scope** - 원래 requirement가 불완전했고 현재 PR이 새 경계를 명시적으로 소유해야 할 때
- **Create a follow-up** - 발견은 유효하지만 현재 requirement 만족에 필요하지 않을 때

RDD는 모든 발견을 새 PR로 만들라고 요구하지 않습니다. 경계 결정을 명시하라고 요구합니다.

## Reviewer 책임

Reviewer는 code quality뿐 아니라 requirement 추적 가능성도 확인해야 합니다.

- Driving requirement가 명확한가?
- Spec이 그 requirement를 표현하는가?
- Test가 의미 있는 rule을 보호하는가?
- Implementation이 숨은 scope growth 없이 requirement를 만족하는가?
- Evidence가 requirement를 직접 뒷받침하는가? `unknown`과 `satisfied`를 분리했는가?
- 구현 중 requirement가 바뀌었는가?

기술적으로 깔끔한 PR도 처음과 다른 문제를 해결한다면 RDD loop로서는 좋지 않을 수 있습니다. 결과는 다음처럼 정방향뿐 아니라 역방향으로도 review합니다.

```text
Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome
```
