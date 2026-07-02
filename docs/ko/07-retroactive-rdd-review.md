# 소급 RDD 리뷰

소급 RDD 리뷰는 처음부터 RDD로 개발되지 않았을 수 있는 기존 프로젝트에 Requirement Driven Development를 적용해 보는 방법입니다.

목적은 프로젝트가 이제 "RDD 적용 완료"라고 선언하는 것이 아닙니다. 목적은 candidate requirement를 복원하고, trace gap을 찾고, 무엇을 현재 프로젝트 truth로 승격할 수 있는지 판단하는 것입니다.

## 언제 사용하는가

다음 상황에서 사용합니다.

- 기존 프로젝트에 spec, test, docs, implementation behavior는 있지만 driving requirement가 불명확한 경우
- 팀이 과거를 다시 쓰지 않고 RDD를 도입하고 싶은 경우
- reviewer가 durable requirement와 implementation choice를 구분해야 하는 경우
- safety 또는 automation boundary가 있어 보이지만 rationale이 문서화되어 있지 않은 경우
- source-of-truth requirement 문서를 쓰기 전에 candidate requirement index가 필요한 경우

## 핵심 규칙

```text
복원된 requirement는 확인되기 전까지 candidate다.
```

기존 동작은 evidence이지 requirement 증명이 아닙니다. Test도 evidence이지 product intent 증명이 아닙니다. 반복되는 제약은 중요할 수 있지만, purpose, rationale, failure prevented를 복원하거나 확인하기 전에는 프로젝트 truth로 승격하지 않아야 합니다.

## 리뷰 순서

1. Current truth를 읽습니다.
   현재 docs, specs, tests, public contracts, safety notes, active task surface에서 시작합니다. 오래된 roadmap note나 완료된 work log보다 현재 truth를 우선합니다.

2. Existing claims를 inventory합니다.
   명시된 spec, invariant, acceptance criteria, non-goal, safety default, 반복되는 constraint를 추출합니다. Implementation fact와 stated behavior contract를 분리합니다.

3. Candidate requirement를 추론합니다.
   중요한 spec이 어떤 사용자, 제품, 비즈니스, 운영, safety, 기술적 필요를 보호하는지 묻습니다. 유용한 candidate requirement는 시스템이 무엇을 하는지가 아니라 왜 그 동작이 중요한지를 설명합니다.

4. Confidence를 표시합니다.

   ```text
   confirmed:
     현재 docs, tests, 또는 사용자 확인에서 직접 표현됨.

   inferred:
     현재 behavior, tests, 반복되는 constraint가 강하게 암시하지만 직접 표현되지는 않음.

   unclear:
     그럴듯하지만 evidence가 부족함.
   ```

5. Change risk를 분리합니다.

   ```text
   change-dangerous:
     해당 spec이 active requirement 또는 safety invariant를 보호하는 것으로 보임.

   change-review-needed:
     해당 spec이 inferred requirement 또는 unresolved assumption과 연결됨.

   change-likely-safe:
     해당 behavior가 product intent보다 implementation choice에 가까워 보임.
   ```

   Traceability가 없다는 것은 자동으로 안전하다는 뜻이 아니라 review-needed입니다.

## Boundary Questions First

pre-RDD 히스토리가 많은 프로젝트에서는 full requirement hierarchy가 이른 경우가 많습니다.

다음이 불명확하면 hierarchy를 만들기 전에 boundary clarification을 합니다.

- 복원된 requirement들이 기여하는 root goal
- rationale 또는 failure prevented
- 어떤 constraint가 durable requirement이고 어떤 것이 implementation choice인지
- state-changing work의 automation boundary
- 사용자가 read-only review, candidate index, confirmed project truth, future loop용 RDD 중 무엇을 원하는지

다음 compact form을 사용합니다.

```text
Boundary Questions First
- Why this is needed:
- Known trace:
- Questions:
  1. ...
- What will be classified after answers:
```

## Retroactive coverage

복원된 requirement를 source-of-truth docs로 승격하기 전에 coverage를 요약합니다.

```text
Retroactive Coverage
- Adoption scope:
- What appears already traceable:
- What is inferred but not confirmed:
- Specs/tests without recovered rationale:
- What should not be called RDD-applied yet:
```

이 요약은 first-pass review가 full adoption으로 오해되는 것을 막습니다.

## Candidate requirement 형태

Evidence가 충분할 때 다음 형태를 사용합니다.

```text
Candidate Requirement
- Title:
  Status: confirmed | inferred | unclear
  Requirement:
  Rationale:
  Failure prevented:
  Assumptions:
  Derived specs/tests:
  Evidence:
  Revisit when:
```

Rationale, failure prevented, assumptions를 복원할 수 없다면 그 항목은 unresolved candidate 또는 trace gap으로 남깁니다.

## Adoption boundary

소급 리뷰와 requirement adoption은 다른 loop입니다.

소급 리뷰는 다음을 만들 수 있습니다.

- coverage summary
- candidate requirements
- trace gaps
- confirmation questions
- change-risk guidance

조용히 다음을 만들면 안 됩니다.

- 완료된 requirement set
- source-of-truth project requirements
- confirmed adoption처럼 보이는 public docs
- implementation changes
- automation policy changes

Candidate requirement를 project truth로 승격하는 일은 별도 forward RDD loop여야 합니다. 그 loop에는 자체 requirement, rationale, failure prevented, review, non-goal이 있어야 합니다.

## 리뷰 출력

Compact retroactive review는 다음 형태를 사용할 수 있습니다.

```text
Root Goal
- Goal:
  Status:
  Rationale:
  Evidence:

Candidate Requirements
- R?: ...

Unresolved Requirement Candidates
- Spec/invariant:
  Possible requirement:
  Missing rationale/assumption:
  Question needed:

Automation Boundary
- Automate now:
- Require human review:
- Do not automate yet:
- Evidence/uncertainty:

Spec Trace
- Spec/invariant:
  Candidate requirement:
  Change risk:
  Notes:

Open Questions
1. ...

Implementation Choices
- Likely safe to change, assuming the candidate requirements remain satisfied:
```

보고서는 자주 읽을 수 있을 만큼 작게 유지합니다. 다음 결정을 위해 필요한 영역만 확장합니다.

## Guardrails

- 모든 기존 behavior를 requirement로 취급하지 않습니다.
- 모든 test를 product intent의 증거로 취급하지 않습니다.
- first-pass candidate hierarchy를 프로젝트가 이제 RDD를 만족한다는 증거로 취급하지 않습니다.
- 복원된 requirement를 확인 없이 current truth라고 부르지 않습니다.
- 별도 adoption loop 없이 retroactive candidate를 public source-of-truth docs로 전환하지 않습니다.
- Implementation convenience가 requirement를 다시 정의하게 두지 않습니다.
- Uncertainty를 지우지 않습니다.
