# RDD 코딩 프롬프트 템플릿

이 task를 요구사항 주도 루프로 수행하세요.

## Requirement

이 task가 만족해야 하는 안정적인 requirement를 적으세요.

다음을 포함하세요.

- 더 큰 제품/운영 방향의 일부라면 root goal
- Rationale: 이 requirement가 중요한 이유
- Failure prevented: 이 requirement가 막는 risk, regression, 나쁜 결과
- 지속 requirement라면 assumptions와 revisit 조건

자동화나 state-changing work라면 다음도 적으세요.

- Automate now
- Require human review
- Do not automate yet

## Spec

Requirement를 표현하는 규칙, 계약, 경계, 인수 기준을 적으세요.

## Tests / Checks

Spec을 보호해야 하는 tests 또는 checks를 적으세요.

## Non-goals

Scope 밖에 있어야 하는 adjacent work를 적으세요.

## 지시사항

- 이 loop에서는 requirement를 안정적으로 유지하세요.
- rationale이 명시되지 않은 구현 선택을 requirement로 취급하지 마세요.
- 장기 goal과 현재 safety stage가 충돌해 보이면 staged requirement로 표현하세요.
- 같은 requirement를 계속 표현하는 경우에만 spec과 test를 refine하세요.
- Requirement가 바뀌는 것처럼 보이면 scope를 확장하기 전에 멈추고 보고하세요.
- Non-goals를 보존하세요.
- 구현 중 편리하다는 이유로 adjacent behavior를 추가하지 마세요.
- 마지막에 final trace를 요약하세요.

```text
Requirement -> Spec -> Tests/Checks -> Implementation
```
