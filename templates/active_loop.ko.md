# Active RDD loop template

Requirement reference: REQ-FIRST-CAPABILITY
Loop unit: 하나의 pull request, task, ticket 또는 local change set
Adoption trigger: 없음, 또는 gate를 연 risk-sensitive condition

## Requirement

이 loop의 안정적인 requirement boundary를 적습니다.

## Spec

이 loop에서 파생한 rule, contract, boundary, acceptance criteria를 적습니다.

## Tests / Checks

Spec을 보호하는 executable test, build, review, manual check를 나열합니다. Requirement를 satisfied, unsatisfied, unknown으로 분류할 수 있는 직접적인 acceptance evidence를 기록합니다. Unknown은 satisfied가 아닙니다.

## Implementation

Requirement와 spec을 만족하는 최소 implementation을 기록합니다.

## Review

`Requirement -> Spec / acceptance -> Implementation / evidence`와 `Implementation / evidence -> Spec / acceptance -> Requirement -> Goal / Outcome` 양방향 trace를 확인합니다. 직접적인 evidence 없이 implementation progress, commit, task 완료를 requirement satisfaction으로 취급하지 않습니다. Boundary decision이 있으면 기록합니다.

Risk-sensitive adoption loop라면 다음도 기록합니다.

- Requirement coverage:
- Derived behavior spec:
- Decision record needed: yes | no
- Validation evidence:

## Non-goals

이 loop 밖에 남겨 둔 adjacent work를 나열합니다.
