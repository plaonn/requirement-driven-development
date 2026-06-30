# 영수증 포맷팅 리팩터링 예시

## Requirement

Pricing 동작을 바꾸지 않고 receipt formatting을 pricing calculation에서 분리합니다.

## Spec

- Pricing totals는 그대로 유지됩니다.
- 영수증 텍스트 포맷팅은 formatter 경계 뒤로 이동합니다.
- 기존 discount 계산 동작은 유지됩니다.
- 유용한 경우 snapshot 또는 golden master test가 output을 보호합니다.

## Tests

- 기존 pricing tests 유지
- 리팩터링 전후 영수증 출력 snapshot 통과
- Discount rule tests 통과

## 구현 참고

Implementation은 외부에서 보이는 pricing 동작을 유지하면서 receipt formatting을 pricing calculation에서 분리해야 합니다.

Pricing path를 건드린다면 totals, discounts, rounding, receipt output이 유지된다는 점을 test로 보여야 합니다.

## 리뷰 초점

- Formatting이 명확한 경계 뒤로 이동했는가?
- Pricing 동작이 유지됐는가?
- Receipt wording 변경이 있다면 의도적이고 문서화되어 있는가?
- PR이 refactoring loop 안에 bug fix를 숨기지 않았는가?

## Requirement 변경 예시

Receipt wording을 의도적으로 바꾸면 동작 또는 spec 변경이므로 명시해야 합니다.

Pricing bug를 발견했다면 현재 loop를 명시적으로 re-scope하지 않는 한 refactoring PR에 숨기지 말고 follow-up을 엽니다.
