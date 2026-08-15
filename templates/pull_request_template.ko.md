# Need / goal context

Loop에 필요한 만큼만 이 template을 사용하세요. 작은 loop는 같은 정보를 간결한 PR 설명이나 다른 기존 review surface에 남길 수 있으며, 별도 heavyweight artifact가 필수는 아닙니다.

어떤 stakeholder 문제, 바람, desired outcome이 이 PR을 정당화합니까?

어떤 requirement source 또는 stakeholder가 그 context를 제공합니까?

# Requirement

이 PR이 만족해야 하는 capability, quality, constraint 또는 condition은 무엇입니까?

이 requirement가 왜 중요합니까?

어떤 실패, regression, risk를 막습니까?

이 PR이 더 큰 root goal의 일부라면 현재 requirement는 어떤 좁은 stage를 다룹니까?

# Requirement validity

Validity scope:
이 항목은 loop-local requirement, durable requirement, temporary/scoped policy 중 무엇입니까?

Assumptions:
Durable이라면 어떤 condition이 계속 참이어야 합니까?

Revisit when:
Durable이라면 어떤 observable signal이 revalidation을 trigger합니까?

Expiration rule:
Temporary 또는 scoped policy라면 어떤 event 또는 condition이 validity를 끝냅니까?

Revalidation outcome:
Revisit signal이 발생했다면 requirement를 retain, narrow, supersede, discard 중 어떻게 처리했습니까?

Affected traces:
어떤 spec, test, implementation, docs, active loop가 영향을 받습니까?

# Decision classification

이 결정은 durable requirement, temporary experiment policy, provider workaround, implementation choice, promotion candidate, expired/superseded policy 중 무엇입니까?

Accepted라면 acceptance scope는 무엇입니까?

Temporary 또는 scoped decision이라면 policy horizon, promotion rule, expiration rule, canonical owner는 무엇입니까?

# Spec

그 requirement를 표현하는 규칙, 경계, API 계약, 인수 기준은 무엇입니까?

# Tests / acceptance evidence

Spec을 보호하는 tests 또는 checks는 무엇이며, requirement가 satisfied, unsatisfied, unknown 중 무엇인지 직접 보여 주는 observable evidence는 무엇입니까?

# Implementation

무엇이 변경됐습니까?

# Non-goals

의도적으로 scope 밖에 둔 것은 무엇입니까?

# Automation boundary

이 PR이 state-changing work를 자동화한다면, 지금 자동화해도 되는 일, 아직 human review가 필요한 일, 아직 자동화하지 말아야 하는 일은 무엇입니까?

# Boundary clarification

Root goal, rationale, failure prevented, decision class, 구현 선택과 requirement의 경계, automation boundary가 불명확했다면 PR scope를 확정하기 전에 어떤 질문에 답했습니까?

# 발견된 requirement 변경

구현이나 review 중 원래 requirement 변경 필요가 드러났습니까?

# 리뷰 초점

Reviewer가 특히 봐야 할 것은 무엇입니까?

Implementation과 evidence를 spec/acceptance를 거쳐 원래 requirement와 goal까지 역추적할 수 있습니까? Commit, task 완료, 관련 없는 test 통과를 requirement evidence로 취급하지 마세요.
