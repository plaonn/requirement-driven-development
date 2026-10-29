# When to Use RDD, and Its Limits

RDD states its own applicability. A team or agent should not need a separate local policy to know how much of RDD a given change deserves, and should not apply the full trace to every change.

## Scale by consequence, not size

Choose intensity by what is lost if the loop's purpose or evidence is wrong, not by line count.

| Level | Use when | Required trace |
| --- | --- | --- |
| 0. None | A question, or a change whose purpose is obvious from the diff and whose effect is local and easily reversible (typo, rename covered by existing tests, dependency bump with passing CI). | Nothing beyond the normal commit message. |
| 1. Minimum trace | Ordinary feature, bug fix, or behavior-preserving refactor. | `Outcome`, `Requirement`, and `Done when` in the PR, task note, or final report. |
| 2. Start and finish gate | The change touches a public contract, authority or permission, data migration, irreversible external effect, financial path, or cross-repository ownership. | Level 1 plus the [risk-sensitive adoption gate](07-retroactive-rdd-review.md#risk-sensitive-forward-adoption-gate). |
| 3. Durable records | Requirements outlive one loop and several loops cite them. | Level 2 plus durable requirement validity fields and, where useful, a decision record. |

Level 0 test: a reviewer can state the purpose and the evidence in one sentence from the diff alone. If they cannot, use Level 1.

Escalation rules:

- If the purpose or boundary turns out to be unclear during the work, move up at least one level and clarify the boundary before continuing.
- If the diff reaches a Level 2 trigger, apply the Level 2 gate even if the loop started lower.
- Do not move down mid-loop merely because the trace is inconvenient.

## Core and optional extensions

Not every part of RDD has the same standing. Adopt the core first; add an extension only when the failure it addresses has actually recurred.

| Part | Status | Why |
| --- | --- | --- |
| Minimum trace (`Outcome`, `Requirement`, `Done when`) | Core | Cheapest form of the loop anchor and the reverse check. |
| Reread the anchor at checkpoints; keep it short enough to reread | Core | Prevents drift when context fades. |
| Autonomy inside the boundary, stop at boundary events | Core | Lets work proceed without approval for refinements. |
| `unknown` is not `satisfied`; delivery signals are not acceptance evidence | Core | Prevents false completion claims. |
| Requirement change is a loop-boundary event; spec and test refinement is not | Core | Detects silent scope change. |
| Rationale and failure prevented on each requirement | Core for durable requirements | The most consistently filled fields in observed use (see Observed usage); usefulness is not measured. |
| Assumptions and revisit signals | Extension for durable requirements | Needed only when a requirement outlives one loop. |
| Hierarchy and semantic identifiers | Extension | Needed only when many requirements need stable references. |
| Active-loop files and `tools/rdd/rdd.py` | Extension | Structural help; not required for the core. |
| Risk-sensitive start and finish gate | Level 2 only | Applied by consequence, not by default. |
| Retroactive review | Extension | Used once when adopting RDD in an existing project. |

## Relationship to existing practice

RDD overlaps with common practice. Where a team already does the following well, adopt only what is missing.

| Existing practice | What it already covers | What RDD adds |
| --- | --- | --- |
| User stories and acceptance criteria | Intended behavior and a pass condition. | A requirement anchor kept separate from the spec, so spec changes are not mistaken for requirement changes. |
| ATDD / BDD | Executable acceptance examples. | `unknown` as a distinct result, and evidence that is not executable (manual checks, document review). |
| Definition of Done | A generic completion checklist. | Completion judged against this loop's requirement, not a generic list. |
| TDD / SDD | Tests and specs as feedback and contract. | A reverse check from evidence and implementation back to the requirement and goal. |
| Architecture decision records | Long-lived design choices. | A rule for when a decision record is required and how a requirement is revalidated. |

If acceptance criteria are already reviewed against every PR, the main additions are the explicit re-scope event, the reverse check, and the validity lifecycle for durable requirements.

## Known costs and failure modes

- **Boundary debate.** The line between requirement and spec is a judgment. If a team spends more effort arguing it than the loop is worth, lower the level or treat the statement as a spec.
- **Form filling.** Filled fields are not evidence. A trace whose `Done when` cannot yield `unsatisfied` is decoration.
- **Unowned revisit signals.** A `Revisit when` entry does nothing unless someone checks it. Check durable requirements when a new loop cites them and when a listed signal event occurs. The requirement's maintainer owns that check.
- **Tooling limits.** `tools/rdd/rdd.py` checks structure and identifier consistency. It cannot judge whether a requirement is correct or whether evidence is direct.
- **Requirement and spec drift.** A requirements document that is edited in a large share of feature commits is probably carrying spec detail. Keep behavior detail in the spec and keep the requirement document stable.
- **Anchor too large to reread.** An anchor that cannot be read in full at a checkpoint does not work as an anchor. Keep a short anchor at the top of a large requirements document and load detail on demand.
- **Maintenance weight.** Each added field, identifier scheme, or gate has a cost. Add structure only when a concrete failure in the [Why this exists](../README.md#why-this-exists) list recurs without it.

## Observed usage

The maintainer applied RDD to six of their own projects of different sizes. A read of their repositories and git history, without measuring outcomes, shows:

- **Fields.** Rationale and failure prevented appear throughout the four larger projects. Assumptions and revisit signals appear only in those same four, which adopted the validity lifecycle. The two smallest projects use essentially none of these fields.
- **Revisit signals did not fire.** Of 15 recorded revisit statuses, 10 read "not observed", 4 note a known open limitation, and 1 records a root requirement superseded by a product-positioning decision. That is the only retained supersede decision. In at least one project the validity lifecycle was added retroactively to existing requirements rather than triggered by a signal.
- **Size.** Requirements documents range from about 100 to about 1,400 lines. The largest are the ones that accumulated per-feature sections.
- **Churn.** Requirements documents were edited in roughly 6% to 48% of commits, highest in the smallest project (48%) and lowest in the largest history (6%). This suggests spec detail living inside requirement documents, which is the drift described above, though the diffs were not reviewed individually.
- **Tooling.** One project's commit messages cite structural checks (`gaps`, `validate`). No project's files reference `tools/rdd/rdd.py` directly.

- **Anchor size.** The largest requirements document is about 30,000 tokens, too large to reread at each checkpoint. Its first 113 lines (root goal, rationale, failure prevented, and a map of requirements) are about 1,700 tokens and already work as a short anchor. The next largest documents are about 18,000 and 11,000 tokens.
- **Spec detail in requirement edits.** In a sample of four recent edits to the largest document, three added implementation-level binding rules (identity matching, key derivation, allowlisted error codes) and one changed an authority boundary (default OAuth scope). The first kind belongs in the spec; the second is a legitimate requirement-level change.

What this does not show: that RDD prevented any defect or scope change. The history shows adoption and process, not effect.

## Evidence status

RDD is a proposed methodology. The examples in this repository are illustrative, and the observed usage above is a single maintainer's projects without outcome measurement. This repository does not claim measured improvement in defect rates or review quality.

A project adopting RDD can evaluate it cheaply by tracking, over a fixed period:

- loops where review found a requirement boundary change that had not been declared,
- loops where acceptance evidence did not bear on the requirement,
- loops whose trace was judged not worth its cost.

If the first two are rare and the third is common, lower the level or stop.
