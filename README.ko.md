# RDD: 요구사항 주도 개발

English: [README.md](README.md)

요구사항 주도 개발(Requirement Driven Development, RDD)은 각 개발 루프를 안정적인 요구사항에 고정하고, 의도에서 구현까지 추적 가능하게 유지하기 위한 가벼운 개발 방법론입니다.

RDD는 pull request, task, ticket, 작은 agile iteration을 하나의 닫힌 루프로 봅니다.

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

RDD는 SDD나 TDD를 대체하지 않습니다. RDD는 그 위에 요구사항 경계를 둡니다. spec과 test는 이해가 깊어지며 다듬어질 수 있지만, 루프를 정의하는 요구사항은 안정적으로 유지되어야 합니다. 요구사항이 바뀌면 루프 경계가 바뀐 것이므로 명시적으로 재범위화해야 합니다.

## 용어 원칙

이 한국어 문서는 개발자가 실제로 쓰는 영어 용어를 일부 유지합니다. 핵심 개념은 처음 등장할 때 한국어와 영어를 함께 사용하고, 이후에는 문맥상 자연스러운 표현을 사용합니다.

- requirement: 요구사항
- spec: 명세 또는 규칙
- test: 테스트 또는 실행 가능한 검사
- implementation: 구현
- review: 리뷰
- loop boundary: 루프 경계

## 핵심 아이디어

각 개발 루프는 다섯 질문에 답해야 합니다.

1. **Requirement** - 이 변경을 이끄는 사용자, 제품, 비즈니스, 기술적 필요는 무엇인가?
2. **Spec** - 그 요구사항을 표현하는 규칙, 경계, 계약, acceptance criteria는 무엇인가?
3. **Test** - spec이 계속 만족됨을 보호하는 실행 가능한 검사는 무엇인가?
4. **Implementation** - test와 원래 requirement를 만족하는 코드나 문서 변경은 무엇인가?
5. **Review** - 최종 변경이 숨은 scope creep 없이 requirement까지 추적되는가?

계층 구분은 다음과 같습니다.

```text
RDD: Are we still solving the right requirement?
SDD: Is the requirement expressed as a coherent spec?
TDD: Is the spec protected by executable tests?
```

## 왜 필요한가

작은 개발 단위는 자주 비슷한 방식으로 흔들립니다.

- PR이 한 목적에서 시작해 다른 목적으로 끝납니다.
- Test는 통과하지만 원래 requirement를 만족하지 못합니다.
- Refactoring PR이 조용히 behavior를 바꿉니다.
- Bug fix PR이 review되지 않은 rule change가 됩니다.
- Acceptance criteria가 없거나, 모호하거나, requirement보다 좁습니다.
- Review가 implementation detail에 집중하다가 requirement traceability를 놓칩니다.

RDD는 이런 실패를 일찍 발견하기 위한 단순한 기준을 제공합니다.

## PR 규모의 RDD

RDD는 pull request 규모에서 특히 유용합니다.

PR은 단순한 코드 변경 묶음이 아니라 작은 requirement-driven loop로 봐야 합니다.

좋은 PR은 다음 관계를 드러냅니다.

```text
Requirement:
  PR이 존재하는 이유

Spec:
  PR이 만족해야 하는 구체적 규칙과 동작

Tests:
  그 규칙을 보호하는 검사

Implementation:
  test와 requirement를 만족하는 최소 변경

Non-goals:
  이 PR에서 의도적으로 제외한 변경
```

## 핵심 규칙

```text
Spec/test refinement may happen inside the loop.
Requirement change means the loop boundary changed.
```

구현이나 리뷰 중 원래 requirement가 잘못됐거나 불완전하다는 사실을 발견할 수 있습니다. 그 자체는 자연스러운 일입니다. 다만 requirement가 바뀌었다면 test 수정이나 spec 보강으로 조용히 흡수하지 말고, PR을 재범위화하거나 분리하거나 follow-up으로 넘겨야 합니다.

## 문서 구조

```text
docs/
  01-methodology.md
  02-rdd-sdd-tdd-loop.md
  03-pr-as-development-loop.md
  04-review-method.md
  05-examples.md
  06-ai-agent-usage.md
  ko/
    01-methodology.md
    02-rdd-sdd-tdd-loop.md
    03-pr-as-development-loop.md
    04-review-method.md
    05-examples.md
    06-ai-agent-usage.md

templates/
  pull_request_template.md
  codex_prompt_template.md
  pull_request_template.ko.md
  codex_prompt_template.ko.md

examples/
  order-cancel-example.md
  refactoring-example.md
  ko/
    order-cancel-example.md
    refactoring-example.md
```

영어 문서가 공개 기본 구조이며, 한국어 문서는 한국어 독자를 위한 companion 문서입니다.

## 라이선스

이 저장소는 **Creative Commons Attribution 4.0 International License (CC BY 4.0)**로 배포됩니다.
