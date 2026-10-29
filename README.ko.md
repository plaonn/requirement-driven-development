# RDD: Requirement Driven Development

English: [README.md](README.md)

이 문서는 짧은 한국어 개요입니다. 정본은 영어 문서이며, 상세 내용은 번역하지 않고 영어 문서로 연결합니다.

**Requirement Driven Development (RDD)** 는 작은 개발 루프(PR, task, ticket, 작은 iteration)를 안정적인 requirement에 고정하고, 의도에서 구현과 관찰 가능한 증거까지 추적할 수 있게 유지하는 가벼운 방법론입니다.

```text
Need / Goal -> Requirement -> Spec -> Implementation -> Test / Acceptance Evidence -> Review
```

## 목적

RDD의 목적은 두 가지입니다. 첫째, context가 흐려져도 처음 잡은 방향을 유지하도록 requirement를 누구의 기억에도 의존하지 않는 앵커로 둡니다. 둘째, requirement 안에 머무는 변경에는 자율성을 보장해 경계 사건에만 결정이 필요하게 합니다. AI agent에 위임하는 경우가 가장 강한 사례지만 사람 개발자도 같은 문제를 겪습니다. 개인 방법론을 그대로 공개한 것이며, 같은 목적을 가졌다면 쓰면 됩니다.

## 핵심

- Requirement가 루프를 정의합니다. Spec과 test는 이해가 깊어지면 바뀔 수 있지만, requirement가 바뀌면 루프를 명시적으로 다시 범위화(re-scope)합니다.
- 증거는 `satisfied`, `unsatisfied`, `unknown`을 구분할 수 있어야 하며 `unknown`은 `satisfied`가 아닙니다.
- 구현 진행, 테스트 통과, commit, task 완료는 전달 신호이지 requirement 충족의 직접 증거가 아닙니다.
- 최소 trace는 `Outcome / Goal`, `Requirement`, `Done when` 세 가지입니다.
- 강도는 크기가 아니라 결과의 중대성으로 조절합니다.
- 최소 trace, `unknown` 규칙, 경계 변경 규칙이 핵심이고 계층, 식별자, validity lifecycle, 도구는 선택 확장입니다.

## 문서 안내

- 개요와 구조: [README.md](README.md)
- 방법론: [docs/01-methodology.md](docs/01-methodology.md)
- 적용 범위와 한계: [docs/09-applicability-and-limits.md](docs/09-applicability-and-limits.md)
- AI agent 사용: [docs/06-ai-agent-usage.md](docs/06-ai-agent-usage.md)
- 기존 프로젝트 소급 적용: [docs/07-retroactive-rdd-review.md](docs/07-retroactive-rdd-review.md)
- 요구공학과의 관계: [docs/08-rdd-and-requirements-engineering.md](docs/08-rdd-and-requirements-engineering.md)

## 라이선스

CC BY 4.0
