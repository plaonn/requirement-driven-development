# Requirement hierarchy template

이 파일을 current truth로 채택하기 전에 example identifier와 내용을 바꿉니다. `ROOT-REQ-*` entry는 정확히 하나만 둡니다. `Previous identifiers`는 명시적 migration에만 추가하고 모든 current reference를 새 primary identifier로 갱신합니다.

## ROOT-REQ-PROJECT-OUTCOME: Project outcome 보존

- Parent: none
- Root goal: 이 hierarchy가 기여하는 더 큰 desired outcome을 적습니다.
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: 계속 참이어야 하는 최상위 capability, quality, constraint 또는 condition을 적습니다.
- Rationale: 이 requirement가 중요한 이유를 설명합니다.
- Failure prevented: Requirement가 약해지거나 제거되면 생길 문제를 설명합니다.
- Assumptions: Requirement를 유효하게 유지하는 condition을 적습니다.
- Derived specs: 이 requirement를 만족하는 current contract를 연결하거나 요약합니다.
- Revisit when: Revalidation을 trigger하는 observable signal을 적습니다.

## REQ-FIRST-CAPABILITY: 첫 capability 보존

- Parent: ROOT-REQ-PROJECT-OUTCOME
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: 계속 참이어야 하는 child capability, quality, constraint 또는 condition을 적습니다.
- Rationale: 이 child requirement가 중요한 이유를 설명합니다.
- Failure prevented: 이 child requirement가 막는 failure를 설명합니다.
- Assumptions: Child requirement를 유효하게 유지하는 condition을 적습니다.
- Derived specs: 이 child requirement를 만족하는 current contract를 연결하거나 요약합니다.
- Revisit when: Revalidation을 trigger하는 observable signal을 적습니다.
