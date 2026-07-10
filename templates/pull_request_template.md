# Need / goal context

What stakeholder problem, desire, or desired outcome justifies this PR?

What requirement source or stakeholder provides that context?

# Requirement

What capability, quality, constraint, or condition must this PR satisfy?

Why does this requirement matter?

What failure, regression, or risk does it prevent?

If this PR belongs to a larger root goal, what narrower stage does this requirement cover?

# Requirement validity

Validity scope:
Is this a loop-local requirement, durable requirement, or temporary/scoped policy?

Assumptions:
If durable, what conditions must remain true?

Revisit when:
If durable, what observable signals should trigger revalidation?

Expiration rule:
If this is a temporary or scoped policy, what event or condition ends its validity?

Revalidation outcome:
If a revisit signal occurred, was the requirement retained, narrowed, superseded, or discarded?

Affected traces:
Which specs, tests, implementation, docs, or active loops are affected?

# Decision classification

Is this a durable requirement, temporary experiment policy, provider workaround, implementation choice, promotion candidate, or expired/superseded policy?

If accepted, what is the acceptance scope?

If this is temporary or scoped, what are the policy horizon, promotion rule, expiration rule, and canonical owner?

# Spec

What rules, boundaries, API contracts, or acceptance criteria express the requirement?

# Tests

What tests or checks protect the spec?

# Implementation

What changed?

# Non-goals

What is intentionally out of scope?

# Automation boundary

If this PR automates state-changing work, what may be automated now, what still requires human review, and what should not be automated yet?

# Boundary clarification

If the root goal, rationale, failure prevented, decision class, implementation-choice boundary, or automation boundary was unclear, what questions were answered before this PR scope was finalized?

# Requirement changes discovered

Did implementation or review reveal that the original requirement needs to change?

# Review focus

What should reviewers pay special attention to?
