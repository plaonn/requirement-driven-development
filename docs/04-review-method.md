# RDD Review Method

RDD review checks whether a development loop remains traceable from requirement to implementation.

Use this checklist for pull requests, tickets, tasks, and small iteration reviews.

## Review checklist

### 1. Requirement

- [ ] Is the driving requirement clear?
- [ ] Does it explain why the work exists, not only what behavior is desired?
- [ ] Does it name the failure, regression, or risk it is meant to prevent?
- [ ] Is it specific enough to distinguish success from unrelated change?
- [ ] Does the PR, task, or ticket still match the stated requirement?
- [ ] If there is a larger root goal, is this loop's narrower requirement clearly staged under it?

### 2. Spec

- [ ] Does the spec express the requirement correctly?
- [ ] Are important rules, boundaries, API contracts, and acceptance criteria visible?
- [ ] Are edge cases handled as spec refinement rather than hidden assumptions?

### 3. Tests

- [ ] Do tests protect meaningful rules?
- [ ] Are tests derived from the spec rather than incidental implementation details?
- [ ] Are important negative cases or boundaries covered?
- [ ] If tests changed, do they still protect the same requirement?

### 4. Implementation

- [ ] Does the implementation satisfy the tests?
- [ ] Does it satisfy the original requirement, not only the tests?
- [ ] Is the change as narrow as the loop requires?
- [ ] Are implementation details consistent with the stated spec?

### 5. Scope

- [ ] Did unrelated behavior enter the loop?
- [ ] Did refactoring introduce behavior changes?
- [ ] Did implementation convenience expand the public contract?
- [ ] Did an implementation choice get promoted into a requirement without rationale?
- [ ] Are adjacent fixes separated or explicitly included?

### 6. Automation boundary

Use this section when the loop automates user, operational, financial, safety-sensitive, or otherwise state-changing work.

- [ ] Is it clear what may be automated now?
- [ ] Is it clear what may be prepared but still requires human review?
- [ ] Is it clear what should not be automated yet?
- [ ] If the long-term goal is broader automation, is the current safety stage explicit?

### 7. Change boundary

- [ ] Did the requirement change during implementation?
- [ ] If it changed, was the loop explicitly re-scoped, split, or restarted?
- [ ] Are requirement changes described where reviewers can see them?

### 8. Non-goals

- [ ] Are excluded items explicit?
- [ ] Are reviewers protected from assuming omitted work is accidental?
- [ ] Are follow-up items separated from the current loop?

## Practical review flow

Start with the requirement, not the diff.

Then read the spec and tests before judging implementation details. This keeps review anchored to the loop boundary and prevents the implementation from silently redefining the goal.

End by checking whether any discoveries during implementation changed the requirement. If they did, treat that as a boundary decision, not just a code review comment.
