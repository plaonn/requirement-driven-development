# Requirement Hierarchy Template

Replace the example identifiers and text before adopting this file as current truth. Keep exactly one `ROOT-REQ-*` entry. Add `Previous identifiers` only for an explicit migration, and update all current references to the new primary identifier.

## ROOT-REQ-PROJECT-OUTCOME: Preserve the project outcome

- Parent: none
- Root goal: State the larger desired outcome this hierarchy serves.
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: State the top-level capability, quality, constraint, or condition that must remain true.
- Rationale: Explain why this requirement matters.
- Failure prevented: Explain what would go wrong if the requirement were weakened or removed.
- Assumptions: State the conditions that keep this requirement valid.
- Derived specs: Link or summarize the current contracts that satisfy this requirement.
- Revisit when: State observable signals that trigger revalidation.

## REQ-FIRST-CAPABILITY: Preserve the first capability

- Parent: ROOT-REQ-PROJECT-OUTCOME
- Decision class: Durable Requirement
- Validity scope: Durable
- Requirement: State the child capability, quality, constraint, or condition that must remain true.
- Rationale: Explain why this child requirement matters.
- Failure prevented: Explain the failure this child requirement prevents.
- Assumptions: State the conditions that keep this child requirement valid.
- Derived specs: Link or summarize the current contracts that satisfy this child requirement.
- Revisit when: State observable signals that trigger revalidation.
