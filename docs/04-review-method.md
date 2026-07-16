# RDD Review Method

RDD review checks whether a development loop remains traceable from requirement to implementation.

Use this checklist for pull requests, tickets, tasks, and small iteration reviews.

## Review checklist

### 1. Requirement

- [ ] Is the stakeholder need or root goal that justifies the loop clear?
- [ ] Is the driving requirement clear?
- [ ] Does the requirement state the capability, quality, constraint, or condition that must be satisfied?
- [ ] Do the linked need, goal, and rationale explain why the work exists?
- [ ] Does it name the failure, regression, or risk it is meant to prevent?
- [ ] Is it specific enough to distinguish success from unrelated change?
- [ ] Does the PR, task, or ticket still match the stated requirement?
- [ ] If there is a larger root goal, is this loop's narrower requirement clearly staged under it?

### 2. Requirement validity

- [ ] Is the item a loop-local requirement, durable requirement, or temporary/scoped policy?
- [ ] If durable, are the assumptions and observable `Revisit when` signals explicit?
- [ ] If it is a temporary or scoped policy, is the expiration rule explicit?
- [ ] Has any assumption failed or revisit signal occurred?
- [ ] If revalidation occurred, is the outcome `retain`, `narrow`, `supersede`, or `discard`?
- [ ] Were affected specs, tests, implementation, docs, and active loops updated or stopped?

### 3. Spec

- [ ] Does the spec express the requirement correctly?
- [ ] Are important rules, boundaries, API contracts, and acceptance criteria visible?
- [ ] Are edge cases handled as spec refinement rather than hidden assumptions?

### 4. Tests

- [ ] Do tests protect meaningful rules?
- [ ] Are tests derived from the spec rather than incidental implementation details?
- [ ] Are important negative cases or boundaries covered?
- [ ] If tests changed, do they still protect the same requirement?

### 5. Implementation

- [ ] Does the implementation satisfy the tests?
- [ ] Does it satisfy the original requirement, not only the tests?
- [ ] Is the change as narrow as the loop requires?
- [ ] Are implementation details consistent with the stated spec?

### 6. Scope

- [ ] Did unrelated behavior enter the loop?
- [ ] Did refactoring introduce behavior changes?
- [ ] Did implementation convenience expand the public contract?
- [ ] Did an implementation choice get promoted into a requirement without rationale?
- [ ] Did a temporary experiment policy or provider workaround get promoted into a durable requirement without a promotion rule?
- [ ] If a decision is accepted, is the acceptance scope explicit?
- [ ] Are adjacent fixes separated or explicitly included?

### 7. Automation boundary

Use this section when the loop automates user, operational, financial, safety-sensitive, or otherwise state-changing work.

- [ ] Is it clear what may be automated now?
- [ ] Is it clear what may be prepared but still requires human review?
- [ ] Is it clear what should not be automated yet?
- [ ] If the long-term goal is broader automation, is the current safety stage explicit?

### 8. Change boundary

- [ ] Did the requirement change during implementation?
- [ ] If it changed, was the loop explicitly re-scoped, split, or restarted?
- [ ] Are requirement changes described where reviewers can see them?

### 9. Non-goals

- [ ] Are excluded items explicit?
- [ ] Are reviewers protected from assuming omitted work is accidental?
- [ ] Are follow-up items separated from the current loop?

### 10. Risk-sensitive adoption evidence

Use this section when the loop triggered the
[existing-project forward adoption gate](07-retroactive-rdd-review.md#risk-sensitive-forward-adoption-gate).

- [ ] Was the relevant requirement source loaded before implementation?
- [ ] Does a specific requirement cover the capability and its authority or failure boundary, rather than relying only on a broad root goal?
- [ ] Is any canonical ownership, trust-boundary, delegated-authority, or rejected-alternative decision preserved when it has long-lived value?
- [ ] Are requirement coverage, derived behavior spec, tests/checks, implementation, and validation evidence all visible?
- [ ] Were the project's selected local or CI checks run for this risk level?

## Practical review flow

Start with the requirement and its validity conditions, not the diff.

If the requirement's root goal, rationale, failure prevented, decision class, implementation-choice boundary, or automation boundary is unclear, do boundary clarification before writing a full trace. Ask the smallest set of questions needed to settle the loop boundary, then continue the review.

Then read the spec and tests before judging implementation details. This keeps review anchored to the loop boundary and prevents the implementation from silently redefining the goal.

End by checking whether any assumption failed, revisit signal occurred, or discovery during implementation changed the requirement. If so, revalidate the requirement and treat the outcome as a boundary decision, not just a code review comment.

For a risk-sensitive adoption loop, passing tests and an updated behavior spec
are necessary evidence but not a complete finish gate. Confirm durable
requirement coverage and any justified decision record before completion.
