# RDD: 요구사항 주도 개발

영어: [README.md](README.md)

요구사항 주도 개발(Requirement Driven Development, RDD)은 각 개발 루프를 안정적인 요구사항에 고정하고, 의도에서 구현까지 추적 가능하게 유지하기 위한 가벼운 개발 방법론입니다.

RDD는 pull request, task, ticket, 작은 agile iteration을 하나의 닫힌 루프로 봅니다.

```text
Requirement -> Spec -> Test -> Implementation -> Review
```

RDD는 SDD나 TDD를 대체하지 않습니다. RDD는 그 위에 요구사항 경계를 둡니다. spec과 test는 이해가 깊어지며 다듬어질 수 있지만, 루프를 정의하는 요구사항은 안정적으로 유지되어야 합니다. 요구사항이 바뀌면 루프 경계가 바뀐 것이므로 명시적으로 re-scope해야 합니다.

## Root goal

RDD는 작은 개발 루프가 그 루프를 정당화하는 need와 goal, 그리고 loop를 고정하는 requirement와 계속 정렬되도록 돕습니다. 그래서 spec, test, implementation, review가 추적 가능하게 남고, scope 변경은 명시적인 결정으로 드러납니다.

## 요구공학과의 관계

RDD는 요구공학(Requirements Engineering)을 대체하지 않습니다. 요구공학은 system 또는 product lifecycle 전체에서 요구사항을 도출하고, 분석하고, 협상하고, 명세하고, 검증하고, 관리하는 더 넓은 분야입니다.

RDD의 경계는 더 좁습니다. 현재 개발 loop에 사용할 candidate requirement가 관련 need 또는 goal에서 파생되고 충분히 도출·검증되었다고 전제한 뒤, 그 requirement가 spec, test, implementation, review까지 추적 가능하게 유지되도록 돕습니다. Stakeholder discovery, product discovery, requirement prioritization, conflict resolution, system-wide requirements management는 RDD가 대체하지 않습니다.

자세한 경계는 [RDD와 요구공학](docs/ko/08-rdd-and-requirements-engineering.md)에서 설명합니다.

## 용어 경계

RDD는 작은 loop의 각 계층을 review할 수 있게 다음과 같은 실용적 용어를 사용합니다.

```text
Need: stakeholder의 문제, 바람, 기대 결과
Goal: 하나 이상의 requirement에 방향을 주는 바람직한 상태
Requirement: 반드시 만족해야 하는 capability, quality, constraint, condition
Spec: requirement를 rule, contract, boundary, acceptance criteria로 정밀하게 표현한 현재 해석
```

Need와 goal은 작업이 왜 존재하고 어느 방향을 향하는지 설명합니다. Requirement는 무엇이 참이어야 하는지 말하며 loop를 고정합니다. Spec은 현재 해석을 verification 가능한 수준으로 구체화합니다. 요구공학에서는 이 용어들을 더 넓은 여러 의미로 사용합니다. 여기의 구분은 보편적 용어를 주장하는 것이 아니라 명시적인 RDD convention입니다.

<!-- companion-only:start -->
## 용어 원칙

이 한국어 문서는 개발자가 실제로 쓰는 영어 용어를 일부 유지합니다. 핵심 개념은 처음 등장할 때 한국어와 영어를 함께 사용하고, 이후에는 문맥상 자연스러운 표현을 사용합니다.

- requirement: 요구사항
- spec: 명세 또는 규칙
- test: 테스트 또는 실행 가능한 검사
- implementation: 구현
- review: 리뷰
- loop boundary: 루프 경계
<!-- companion-only:end -->

## 핵심 아이디어

Loop를 열기 전에 candidate requirement를 정당화하는 need 또는 goal을 확인합니다. 그다음 각 개발 loop는 다섯 질문에 답해야 합니다.

1. **Requirement** - 이 loop에서 반드시 만족해야 하는 capability, quality, constraint, condition은 무엇인가?
2. **Spec** - 그 요구사항을 표현하는 규칙, 경계, 계약, 인수 기준은 무엇인가?
3. **Test** - spec이 계속 만족됨을 보호하는 실행 가능한 검사는 무엇인가?
4. **Implementation** - test와 원래 requirement를 만족하는 코드나 문서 변경은 무엇인가?
5. **Review** - 최종 변경이 숨은 scope creep 없이 requirement까지 추적되는가?

계층 구분은 다음과 같습니다.

```text
RDD: 우리는 여전히 올바른 요구사항을 해결하고 있는가?
SDD: 요구사항이 일관된 명세로 표현되어 있는가?
TDD: 명세가 실행 가능한 테스트로 보호되고 있는가?
```

## 왜 필요한가

작은 개발 단위는 자주 비슷한 방식으로 흔들립니다.

- PR이 한 목적에서 시작해 다른 목적으로 끝납니다.
- Test는 통과하지만 원래 requirement를 만족하지 못합니다.
- Refactoring PR이 조용히 동작을 바꿉니다.
- Bug fix PR이 리뷰되지 않은 규칙 변경이 됩니다.
- 인수 기준이 없거나, 모호하거나, requirement보다 좁습니다.
- Review가 구현 세부사항에 집중하다가 requirement 추적 가능성을 놓칩니다.

RDD는 이런 실패를 일찍 발견하기 위한 단순한 기준을 제공합니다.

## RDD 루프

```text
1. 현재 loop의 requirement를 고정한다.
2. Requirement에서 spec을 파생한다.
3. Spec에서 test를 파생한다.
4. Loop가 요구하는 것만 구현한다.
5. Requirement에서 implementation까지 전체 trace를 review한다.
6. Requirement가 바뀌면 loop를 명시적으로 re-scope한다.
```

핵심 구분은 다음과 같습니다.

```text
Loop 안에서 spec/test를 다듬는 것은 정상이다.
Requirement 변경은 loop boundary가 바뀐 것이다.
```

## Requirement validity lifecycle

RDD는 기존 requirement가 더 이상 유효하지 않을 수 있는 순간을 인식할 수 있게 해야 합니다. Test가 통과한다는 이유로 requirement가 여전히 필요하다고 가정하지 않고, requirement가 stale해지기 전에 validity condition을 기록합니다.

```text
Validity scope:
  Loop-local requirement | Durable requirement | Temporary/scoped policy

Assumptions:
  Requirement가 유효하려면 계속 참이어야 하는 condition

Revisit when:
  Revalidation을 trigger하는 observable signal
```

Temporary 또는 scoped constraint는 durable requirement set으로 승격하지 않고 expiration rule을 가진 policy로 유지하는 것이 기본입니다. Revisit signal이 발생했다고 requirement가 자동으로 invalid되는 것은 아닙니다. 그것은 boundary event입니다. 연결된 need, goal, rationale, assumptions를 revalidate한 뒤 requirement를 `retain`, `narrow`, `supersede`, `discard` 중 하나로 명시적으로 처리합니다. 그 결정을 영향받는 spec, test, implementation, active loop에 전파합니다.

## Requirement identifier

RDD는 하나의 identifier 형식을 강제하지 않습니다. `R0`, `R1`, `R2` 같은 기존 numeric hierarchy도 계속 유효합니다. 안정적인 semantic reference가 필요한 프로젝트는 root requirement에 `ROOT-REQ-*`, 그 descendant에 `REQ-*` identifier를 사용할 수 있습니다. Root goal은 hierarchy root 가까이에 있더라도 requirement가 되는 것이 아니라 별도의 justification context로 남습니다.

Semantic identifier는 안정적인 current-truth reference입니다. 한번 채택하면 조용히 rename, reuse, renumber하지 않습니다. Numeric identifier에서의 migration은 선택 사항이며, 과거를 다시 쓰지 않고 old-to-new mapping을 명시적으로 보존해야 합니다.

## RDD 구조와 tooling 도입

기존 numeric RDD project는 hierarchy-only validation부터 시작할 수 있으며 active-loop directory를 만들거나 identifier를 migration할 필요가 없습니다. 새 semantic project는 [requirement hierarchy template](templates/requirements.ko.md)에서 시작할 수 있습니다. Requirement detail을 분리한 project는 여러 file 또는 directory를 하나의 source set으로 전달할 수 있습니다.

```sh
python3 tools/rdd/rdd.py validate REQUIREMENTS.md
python3 tools/rdd/rdd.py validate REQUIREMENTS.md docs/requirements/
```

Disposable active-loop pattern을 선택한 project는 [active-loop template](templates/active_loop.ko.md)에서 시작하고, 작업 중에는 `--loops`를 추가하며, `ready`를 merge-ready structural check로 사용할 수 있습니다. Persistent 또는 selective-retention project는 `ready`를 사용하지 않거나 전용 active-work directory만 대상으로 지정할 수 있습니다.

```sh
python3 tools/rdd/rdd.py validate REQUIREMENTS.md --loops rdd/loops/
python3 tools/rdd/rdd.py ready REQUIREMENTS.md --loops rdd/loops/
```

## 기존 프로젝트

기존 프로젝트에 RDD를 적용할 때는 기존 spec, test, 구현 동작을 confirmed requirement의 증명으로 취급하지 않습니다.

먼저 [소급 RDD 리뷰](docs/ko/07-retroactive-rdd-review.md)에서 시작합니다. 첫 pass는 read-only로 두고, candidate requirement를 복원하고, trace gap을 찾고, 무엇을 source-of-truth 문서로 승격하기 전에 확인해야 하는지 정합니다.

`SPEC.md`, roadmap, test suite, 안정적인 구현은 유용한 evidence가 될 수 있지만 그 자체로 충분하지 않습니다. Root goal, rationale, failure prevented, loop boundary가 빠져 있거나 불명확하면 복원된 항목은 candidate로 유지하고, 구현이나 문서 adoption 전에 boundary를 먼저 확인합니다.

확인된 decision 중 일부는 durable requirement가 아니라 scoped policy로 남아야 합니다. Temporary experiment policy, provider workaround, operator-run-specific risk decision에는 acceptance scope, promotion rule, expiration rule을 붙여 임시 조건이 실수로 영구 requirement처럼 굳어지지 않게 합니다.

### 위험 기반 forward adoption

첫 retroactive pass 이후 기존 프로젝트의 모든 변경에 무거운 RDD 절차를 적용할 필요는 없습니다. Substantial public capability, OAuth scope, state-changing adapter, irreversible external effect, 금융 또는 live execution path, cross-repository ownership, authority, trust boundary를 추가하는 변경에는 명시적인 start gate와 finish gate를 사용합니다.

시작할 때 관련 requirement source를 읽고, 새 capability와 failure boundary가 구체적인 loop-local 또는 durable requirement로 cover되는지 확인합니다. Broad root goal이 확장을 허용한다는 사실만으로 충분한 coverage가 되지는 않습니다. 완료할 때 spec, test, implementation, 장기 architecture decision까지 trace를 검증합니다. 자세한 내용은 [기존 프로젝트 adoption gate](docs/ko/07-retroactive-rdd-review.md#위험-기반-forward-adoption-gate)를 참고합니다.

## PR 규모의 RDD

RDD는 pull request 규모에서 특히 유용합니다.

PR은 단순한 코드 변경 묶음이 아니라 작은 요구사항 주도 루프로 봐야 합니다.

Pull request를 사용하지 않는 프로젝트에서는 같은 모델을 task 또는 change set 규모에 적용할 수 있습니다. 이때 review surface는 task note, commit message body, agent final trace 같은 가벼운 기록이 될 수 있으며, 핵심은 requirement boundary가 보이게 남는 것입니다.

프로젝트는 완료된 loop record를 계속 보존하거나, 살아남아야 할 truth를 승격한 뒤 disposable active-loop 파일을 삭제하거나, 가치가 높은 record만 선택적으로 보존할 수 있습니다. RDD는 하나의 retention policy를 강제하지 않습니다. 완료 전에 loop boundary를 review할 수 있어야 하며, durable requirement, current contract, test, 중요한 architecture decision은 적절한 current-truth surface에 남아야 합니다.

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

## Requirement가 바뀔 때

구현이나 review 중 원래 requirement가 잘못됐거나 불완전하다는 사실을 발견할 수 있습니다.

이것은 단순한 test update가 아니라 loop boundary event입니다.

다음 중 하나를 선택할 수 있습니다.

- PR을 re-scope하고 requirement를 명시적으로 갱신합니다.
- 현재 PR은 최소 범위로 유지하고 follow-up을 만듭니다.
- 관련 없는 발견은 별도 loop로 분리합니다.

## 문서 구조

```text
docs/
  01-methodology.md
  02-rdd-sdd-tdd-loop.md
  03-pr-as-development-loop.md
  04-review-method.md
  05-examples.md
  06-ai-agent-usage.md
  07-retroactive-rdd-review.md
  08-rdd-and-requirements-engineering.md
  ko/
    01-methodology.md
    02-rdd-sdd-tdd-loop.md
    03-pr-as-development-loop.md
    04-review-method.md
    05-examples.md
    06-ai-agent-usage.md
    07-retroactive-rdd-review.md
    08-rdd-and-requirements-engineering.md

skills/
  rdd-retroactive-review/
    SKILL.md

templates/
  requirements.md
  active_loop.md
  pull_request_template.md
  codex_prompt_template.md
  requirements.ko.md
  active_loop.ko.md
  pull_request_template.ko.md
  codex_prompt_template.ko.md

examples/
  order-cancel-example.md
  refactoring-example.md
  ko/
    order-cancel-example.md
    refactoring-example.md
```

## Companion 문서 정책

영어 문서가 canonical public structure입니다. 한국어 companion은 문장별 직역이 아니라 자연스러운 한국어를 사용하되, 같은 reader-facing 개념, 규칙, non-goal, 경고, 예시, section structure를 보존합니다.

영어 문서의 reader-facing 의미가 바뀌면 같은 변경에서 한국어 companion도 갱신합니다. 의도적인 한국어 전용 설명은 `companion-only` comment로 표시합니다. 구조 drift는 `python3 tools/check_companion_docs.py`로 검사하고, 의미 동등성은 review에서 별도로 확인합니다. CI는 push와 pull request마다 구조 검사를 실행합니다.

`skills/` 디렉터리는 공개 방법론을 agent workflow로 적용하기 위한 optional 지침입니다. RDD 자체는 agent-specific 방법론이 아닙니다.

## 라이선스

이 저장소는 **Creative Commons Attribution 4.0 International License (CC BY 4.0)**로 배포됩니다.
