# 개발 루프로서의 PR

RDD에서 pull request는 단순한 코드 변경 묶음이 아닙니다. PR은 다음 흐름을 가진 작은 개발 루프입니다.

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

## 하나의 안정적인 목적

PR은 하나의 안정적인 requirement 또는 목적을 가져야 합니다. 그것은 기능, 버그 수정, 리팩터링, 마이그레이션, 문서 변경, 운영 개선일 수 있습니다.

핵심은 PR이 아주 작아야 한다는 뜻이 아닙니다. Reviewer가 어떤 requirement가 루프 경계를 정의하는지 알 수 있어야 한다는 뜻입니다.

## PR 추적 가능성

좋은 PR 설명은 의도에서 code까지의 경로를 드러냅니다.

```text
Requirement:
  이 PR이 만족하는 필요

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

## Scope creep 감지

Scope creep은 requirement와 연결되지 않은 유용해 보이는 작업으로 나타나는 경우가 많습니다.

Reviewer는 다음을 확인해야 합니다.

- 관련 없는 동작 변경
- 동작 변경을 숨긴 refactoring
- 구현 중 발견된 bug fix가 같은 PR에 섞인 경우
- 명시된 requirement 밖의 동작을 보호하는 test
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
- 구현 중 requirement가 바뀌었는가?
