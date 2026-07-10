# RDD and Requirements Engineering

Requirement Driven Development (RDD) is related to requirements engineering, but it does not replace the broader discipline.

## Requirements engineering scope

Requirements engineering addresses the systematic work needed to understand stakeholder needs and reduce the risk of delivering a system that does not satisfy them. Its activities commonly include:

- identifying requirement sources and stakeholders,
- eliciting candidate requirements,
- analyzing feasibility, ambiguity, dependencies, and conflicts,
- negotiating and prioritizing requirements,
- specifying functional requirements, quality requirements, and constraints,
- validating requirements against stakeholder needs,
- managing requirement versions, changes, and traceability throughout the lifecycle.

These activities may be iterative. Requirements engineering is not limited to an upfront requirements document, and it is not completed merely because implementation has started.

## RDD scope

RDD addresses a narrower problem:

```text
Given a candidate requirement for the current development loop,
keep the loop traceable from that requirement through review.
```

RDD assumes that the candidate requirement has been sufficiently elicited and validated to serve as the current loop boundary. It then connects:

```text
Requirement -> Spec -> Test/Check -> Implementation -> Review
```

RDD is primarily concerned with:

- preserving the purpose and boundary of a small development loop,
- deriving specs and tests from the loop requirement,
- detecting implementation-driven scope growth,
- making requirement changes explicit,
- deciding whether to re-scope, split, or create a follow-up loop,
- keeping the final change traceable to the requirement that justified it.

## What RDD does not replace

RDD does not provide a complete method for:

- discovering all relevant stakeholders,
- eliciting unknown or conflicting needs,
- conducting market or product discovery,
- resolving stakeholder conflicts,
- prioritizing requirements across a product or portfolio,
- analyzing system-wide feasibility,
- maintaining a complete requirements baseline or traceability model,
- validating that the product as a whole satisfies stakeholder and business needs.

Use suitable requirements engineering, product discovery, domain analysis, safety, security, or governance practices for those responsibilities. RDD can consume their results as candidate requirements for a small development loop.

RDD distinguishes the context that justifies a loop from the requirement that anchors it. See [RDD Methodology — Vocabulary boundary](01-methodology.md#vocabulary-boundary) for the explicit `Need`, `Goal`, `Requirement`, `Spec`, and `Implementation choice` convention.

## Where they meet

RDD applies several requirements engineering concerns at task, ticket, pull request, or small-iteration scale:

| Requirements engineering concern | RDD application |
| --- | --- |
| Traceability | Connect the loop requirement to spec, tests, implementation, and review. |
| Change management | Treat a requirement change as an explicit loop-boundary event. |
| Scope control | Split, re-scope, or defer work that no longer belongs to the requirement. |
| Specification | Refine rules, contracts, boundaries, and acceptance criteria inside the loop. |
| Verification | Use tests and checks to assess whether the implementation satisfies the current spec. |
| Validation | Review whether the completed change still addresses the need that justified the loop. |

The RDD trace is intentionally lightweight. Projects that need lifecycle-wide traceability should also maintain links to requirement sources, stakeholders, dependent requirements, architecture, releases, and other relevant work products.

## Practical handoff into an RDD loop

Before treating a candidate requirement as the loop anchor, confirm enough context to avoid inventing the boundary:

```text
Source or stakeholder:
  Where did this need come from?

Need or root goal:
  What problem, desire, or desired state justifies this loop?

Candidate requirement:
  What capability, quality, constraint, or condition must be true for this loop?

Rationale and failure prevented:
  Why does it matter, and what goes wrong without it?

Validation evidence:
  Why is this an adequate requirement for the current loop?

Known conflicts or dependencies:
  What other needs or constraints affect it?
```

Small and obvious changes do not need a long intake record. When the source, purpose, conflict, or adequacy of the candidate requirement is unclear, clarify that boundary before deriving the full RDD trace.

## References

- [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html)
- [IEEE Computer Society — SWEBOK Guide software requirements topics](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics)
- [IREB — CPRE glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary)
