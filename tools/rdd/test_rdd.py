#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import rdd


SAMPLE = """# Example

```text
# Requirement
This heading is inside a fence and should be ignored.
```

## Root goal
Keep development loops traceable.

## Need
Reviewers need to recover why each loop exists.

## Requirement
Extract explicit trace sections.

## Requirement validity
Validity scope: Loop-local.
Revisit signal status: Not observed.

## Rationale
Reduce token cost.

## Failure prevented
Avoid inventing missing requirements.

## Spec
- Parse ATX headings.

## Tests
- Ignore fenced headings.

## Non-goals
- Do not write source files.
"""

HIERARCHY_SAMPLE = """# Requirements

## Requirement Hierarchy

### R0: Reduce attention

- Status: confirmed
- Requirement: Reduce operator attention for asset management.
- Rationale: Avoid repeated manual account checks.
- Failure prevented: Building unrelated provider experiments.
- Assumptions: Read-only analysis comes first.
- Revisit when: Full automation is considered.

### R1: Keep analysis read-only

- Status: confirmed
- Requirement: Analysis commands must not submit orders.
- Rationale: Reports should be safe to run repeatedly.
- Failure prevented: Read-only reports causing live side effects.
"""

KOREAN_HIERARCHY_SAMPLE = """# 요구사항 계층 문서

## R0: 토큰 낭비를 줄이는 안전한 스케줄링

상태: 활성
요구사항: 실행 가능한 작업이 있을 때만 Codex를 호출한다.
근거: 반복 polling에서 불필요한 토큰 사용을 줄여야 한다.
방지 실패: 대기 작업이 없는데도 Codex를 호출하는 상태.
파생 규칙: pause, cooldown, dependency gate를 먼저 평가한다.
재검토 시점: 실행 모델이 바뀔 때.

## R1: 리뷰 전 적용 금지

요구사항: 완료된 작업은 리뷰 전 source-of-truth에 반영하지 않는다.
근거: worker 결과와 운영자 승인 상태를 분리해야 한다.
방지 실패: 검토되지 않은 변경이 완료로 취급되는 상태.
"""

RETROACTIVE_REVIEW_SAMPLE = """# Retroactive Review

## Root Goal

- Goal: Adopt RDD without rewriting existing project history.
  Rationale: The project already has specs and tests but incomplete requirement trace.

## Retroactive Coverage

- What appears already traceable: review/apply safety behavior.
- What is inferred but not confirmed: long-term automation direction.
- Specs/tests without recovered rationale: legacy retry behavior.

## Candidate Requirements

- R1: Keep review state trustworthy
  Requirement: Accept/apply output must agree with persisted task state.
  Rationale: Operators decide whether to retry or clean up from this output.
  Failure prevented: A successful mutation appearing as a lock failure.
  Decision class: Durable Requirement.
  Derived specs/tests: idempotent already-applied accept returns success.
  Revisit when: accept/apply state transitions are redesigned.

## Decision Register

- D1: Limit US live beta orders
  Decision class: Temporary Experiment Policy.
  Durability: Temporary.
  Acceptance scope: beta-only policy accepted.
  Policy horizon: Next manual review.
  Promotion rule: Promote only if repeated across markets or providers.
  Expiration rule: Expires after the beta run or superseding review.
  Canonical owner: Operations lead.

## Automation Boundary

- Automate now: read-only review bundle generation.
- Require human review: source-of-truth requirement adoption.
- Do not automate yet: broad policy changes.

## Non-goals

- Do not rewrite historical task logs.
"""


def semantic_entry(key: str, title: str, parent: str, *, previous: str | None = None) -> str:
    previous_line = f"- Previous identifiers: {previous}\n" if previous else ""
    return (
        f"## {key}: {title}\n\n"
        f"- Parent: {parent}\n"
        "- Decision class: Durable Requirement\n"
        "- Validity scope: Durable\n"
        f"- Requirement: {title}.\n"
        f"- Rationale: {title} matters.\n"
        f"- Failure prevented: Losing {title.lower()}.\n"
        "- Assumptions: The project still needs this requirement.\n"
        "- Derived specs: Current contracts preserve this requirement.\n"
        "- Revisit when: The project boundary changes.\n"
        f"{previous_line}"
    )


def semantic_requirements(*children: str, root_key: str = "ROOT-REQ-TRACEABLE-LOOPS") -> str:
    return "# Requirements\n\n" + semantic_entry(
        root_key,
        "Keep loops traceable",
        "none",
        previous="R0",
    ) + "\n" + "\n".join(children)


def valid_loop(reference: str = "REQ-READ-ONLY") -> str:
    return f"""# Read-only loop

Requirement reference: {reference}
Loop unit: one pull request

## Spec

## Tests / Checks

## Implementation

## Review

## Non-goals
"""


class RddToolTest(unittest.TestCase):
    def test_trace_extracts_expected_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text(SAMPLE, encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(trace["schema_version"], "rdd.trace.v1")
        self.assertEqual(
            trace["fields"]["need"][0]["text"],
            "Reviewers need to recover why each loop exists.",
        )
        self.assertIn("requirement", trace["fields"])
        self.assertEqual(
            trace["fields"]["revisit_signal_status"][0]["text"],
            "Not observed.",
        )
        self.assertEqual(trace["fields"]["requirement"][0]["text"], "Extract explicit trace sections.")
        self.assertNotIn("This heading is inside a fence", json.dumps(trace, ensure_ascii=False))

    def test_gaps_reports_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text("# Requirement\n\nOnly one field.\n", encoding="utf-8")
            trace = rdd.build_trace(path)

        gap_fields = {gap["field"] for gap in trace["gaps"]}
        self.assertIn("rationale", gap_fields)
        self.assertIn("failure_prevented", gap_fields)
        self.assertIn("validity_scope", gap_fields)
        self.assertIn("automation_boundary", gap_fields)

    def test_durable_requirement_requires_validity_conditions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "durable.md"
            path.write_text(
                "# Requirement validity\n\nValidity scope: Durable.\n",
                encoding="utf-8",
            )
            trace = rdd.build_trace(path)

        gap_fields = {gap["field"] for gap in trace["gaps"]}
        self.assertIn("assumptions", gap_fields)
        self.assertIn("revisit_when", gap_fields)

    def test_temporary_requirement_requires_expiration_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "temporary.md"
            path.write_text(
                "# Requirement validity\n\nValidity scope: Temporary/scoped.\n",
                encoding="utf-8",
            )
            trace = rdd.build_trace(path)

        gap_fields = {gap["field"] for gap in trace["gaps"]}
        self.assertIn("expiration_rule", gap_fields)

    def test_validity_conditions_satisfy_conditional_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            durable = root / "durable.md"
            durable.write_text(
                "# Requirement validity\n\n"
                "Validity scope: Durable requirement.\n"
                "Assumptions: The operating boundary remains reliable.\n"
                "Revisit when: The operating boundary changes.\n",
                encoding="utf-8",
            )
            temporary = root / "temporary.md"
            temporary.write_text(
                "# Requirement validity\n\n"
                "Validity scope: Temporary/scoped policy.\n"
                "Expiration rule: The experiment ends.\n",
                encoding="utf-8",
            )

            durable_trace = rdd.build_trace(durable)
            temporary_trace = rdd.build_trace(temporary)

        durable_gaps = {gap["field"] for gap in durable_trace["gaps"]}
        temporary_gaps = {gap["field"] for gap in temporary_trace["gaps"]}
        self.assertNotIn("assumptions", durable_gaps)
        self.assertNotIn("revisit_when", durable_gaps)
        self.assertNotIn("expiration_rule", temporary_gaps)

    def test_directory_scan_skips_private_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "public.md"
            private_dir = root / ".private"
            private_dir.mkdir()
            private_file = private_dir / "private.md"
            public.write_text("# Requirement\n\nPublic.\n", encoding="utf-8")
            private_file.write_text("# Requirement\n\nPrivate.\n", encoding="utf-8")

            trace = rdd.build_trace(root)

        texts = [item["text"] for item in trace["fields"]["requirement"]]
        self.assertEqual(texts, ["Public."])

    def test_numbered_heading_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.md"
            path.write_text("### 1. Requirement\n\nNumbered heading.\n", encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(trace["fields"]["requirement"][0]["text"], "Numbered heading.")

    def test_rdd_hierarchy_bullet_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(HIERARCHY_SAMPLE, encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(trace["fields"]["root_goal"][0]["heading"], "R0: Reduce attention")
        self.assertEqual(
            trace["fields"]["root_goal"][0]["text"],
            "Reduce operator attention for asset management.",
        )
        self.assertEqual(len(trace["fields"]["requirement"]), 2)
        self.assertIn("rationale", trace["fields"])
        self.assertIn("failure_prevented", trace["fields"])
        self.assertEqual(trace["fields"]["assumptions"][0]["text"], "Read-only analysis comes first.")
        self.assertNotIn("spec", trace["fields"])

    def test_semantic_hierarchy_extracts_root_and_child_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(
                semantic_requirements(
                    semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
                ),
                encoding="utf-8",
            )
            trace = rdd.build_trace(path)

        headings = [item["heading"] for item in trace["fields"]["requirement"]]
        self.assertIn("ROOT-REQ-TRACEABLE-LOOPS: Keep loops traceable", headings)
        self.assertIn("REQ-READ-ONLY: Keep analysis read-only", headings)
        self.assertEqual(trace["schema_version"], "rdd.trace.v1")

    def test_semantic_heading_title_is_requirement_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(
                "## ROOT-REQ-TRACEABLE-LOOPS: Keep loops traceable\n\n"
                "## REQ-READ-ONLY: Keep analysis read-only\n",
                encoding="utf-8",
            )
            trace = rdd.build_trace(path)

        texts = [item["text"] for item in trace["fields"]["requirement"]]
        self.assertIn("Keep loops traceable", texts)
        self.assertIn("Keep analysis read-only", texts)

    def test_semantic_hierarchy_requires_exactly_one_root(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-MISSING")
        missing_root_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries("# Requirements\n\n" + child)
        )
        duplicate_root_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(
                semantic_requirements()
                + "\n"
                + semantic_entry("ROOT-REQ-SECOND-GOAL", "Keep another root", "none")
            )
        )

        self.assertIn("semantic_root_count", {issue.code for issue in missing_root_issues})
        self.assertIn("semantic_root_count", {issue.code for issue in duplicate_root_issues})

    def test_semantic_hierarchy_rejects_duplicate_key(self):
        duplicate = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements(duplicate, duplicate))
        )

        self.assertIn("duplicate_key", {issue.code for issue in issues})

    def test_numeric_hierarchy_remains_valid_without_semantic_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(HIERARCHY_SAMPLE, encoding="utf-8")
            (loops / "legacy-loop.md").write_text(valid_loop("R1"), encoding="utf-8")

            issues, _active = rdd.validate_structure([requirements], loops, [])

        self.assertEqual(issues, [])

    def test_validation_rejects_invalid_or_mixed_primary_identifiers(self):
        invalid = semantic_entry("REQ-lowercase", "Use an invalid key", "ROOT-REQ-TRACEABLE-LOOPS")
        invalid_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements(invalid))
        )
        mixed_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements() + "\n" + HIERARCHY_SAMPLE)
        )

        self.assertIn("invalid_requirement_identifier", {issue.code for issue in invalid_issues})
        self.assertIn("mixed_hierarchy", {issue.code for issue in mixed_issues})

    def test_semantic_hierarchy_rejects_missing_parent_and_cycle(self):
        missing_parent = semantic_entry("REQ-MISSING-PARENT", "Require a parent", "REQ-NOT-DEFINED")
        missing_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements(missing_parent))
        )
        cycle_issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(
                semantic_requirements(
                    semantic_entry("REQ-CYCLE-A", "Cycle A", "REQ-CYCLE-B"),
                    semantic_entry("REQ-CYCLE-B", "Cycle B", "REQ-CYCLE-A"),
                )
            )
        )

        self.assertIn("missing_parent", {issue.code for issue in missing_issues})
        self.assertIn("hierarchy_cycle", {issue.code for issue in cycle_issues})

    def test_semantic_hierarchy_requires_durable_fields(self):
        incomplete = """## REQ-INCOMPLETE: Incomplete requirement

- Parent: ROOT-REQ-TRACEABLE-LOOPS
- Requirement: Stay incomplete.
"""
        issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements(incomplete))
        )

        missing_messages = [issue.message for issue in issues if issue.code == "missing_required_field"]
        self.assertTrue(any("Rationale" in message for message in missing_messages))
        self.assertTrue(any("Revisit When" in message for message in missing_messages))

    def test_semantic_root_requires_root_parent_and_durable_decision_class(self):
        invalid_root = semantic_entry(
            "ROOT-REQ-TRACEABLE-LOOPS",
            "Keep loops traceable",
            "REQ-OTHER",
        ).replace("Decision class: Durable Requirement", "Decision class: Implementation Choice")
        issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries("# Requirements\n\n" + invalid_root)
        )

        codes = {issue.code for issue in issues}
        self.assertIn("invalid_root_parent", codes)
        self.assertIn("invalid_root_decision_class", codes)

    def test_previous_identifier_is_not_a_current_loop_reference(self):
        child = semantic_entry(
            "REQ-READ-ONLY",
            "Keep analysis read-only",
            "ROOT-REQ-TRACEABLE-LOOPS",
            previous="R1",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(semantic_requirements(child), encoding="utf-8")
            (loops / "read-only-loop.md").write_text(valid_loop("R1"), encoding="utf-8")

            issues, _active = rdd.validate_structure([requirements], loops, [])

        self.assertIn("undefined_requirement_reference", {issue.code for issue in issues})

    def test_previous_identifier_is_not_a_current_parent_reference(self):
        child = semantic_entry(
            "REQ-CHILD",
            "Keep the child requirement",
            "R1",
        )
        parent = semantic_entry(
            "REQ-PRIMARY-PARENT",
            "Keep the primary parent",
            "ROOT-REQ-TRACEABLE-LOOPS",
            previous="R1",
        )
        issues, _aliases = rdd.validate_requirement_hierarchy(
            self._entries(semantic_requirements(parent, child))
        )

        self.assertIn("missing_parent", {issue.code for issue in issues})

    def test_loop_validation_rejects_undefined_reference_filename_and_metadata(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(semantic_requirements(child), encoding="utf-8")
            (loops / "Bad_Name.md").write_text("# Invalid\n\nRequirement reference: REQ-UNKNOWN\n", encoding="utf-8")

            issues, _active = rdd.validate_structure(
                [requirements],
                loops,
                [],
                r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$",
            )

        codes = {issue.code for issue in issues}
        self.assertIn("invalid_loop_filename", codes)
        self.assertIn("undefined_requirement_reference", codes)
        self.assertIn("missing_loop_metadata", codes)
        self.assertIn("missing_loop_section", codes)

    def test_validate_allows_active_loop_and_ready_rejects_it(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(semantic_requirements(child), encoding="utf-8")
            (loops / "read-only-loop.md").write_text(valid_loop(), encoding="utf-8")

            validate_code, validate_output = self._run_main(["validate", str(requirements), "--loops", str(loops)])
            ready_code, ready_output = self._run_main(["ready", str(requirements), "--loops", str(loops)])

        self.assertEqual(validate_code, 0)
        self.assertIn("No structural contract violations", validate_output)
        self.assertEqual(ready_code, 1)
        self.assertIn("active_loop_remaining", ready_output)

    def test_validate_can_check_hierarchy_without_loop_policy(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        with tempfile.TemporaryDirectory() as tmp:
            requirements = Path(tmp) / "requirements.md"
            requirements.write_text(semantic_requirements(child), encoding="utf-8")

            code, output = self._run_main(["validate", str(requirements)])

        self.assertEqual(code, 0)
        self.assertIn("Active loop validation: not requested", output)

    def test_validate_combines_multiple_requirement_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "REQUIREMENTS.md"
            details = root / "requirements"
            details.mkdir()
            requirements.write_text(semantic_requirements(), encoding="utf-8")
            (details / "read-only.md").write_text(
                semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS"),
                encoding="utf-8",
            )

            issues, _active = rdd.validate_structure([requirements, details], None, [])

        self.assertEqual(issues, [])

    def test_loop_filename_pattern_is_project_selected(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(semantic_requirements(child), encoding="utf-8")
            (loops / "Team_123.md").write_text(valid_loop(), encoding="utf-8")

            default_issues, _active = rdd.validate_structure([requirements], loops, [])
            strict_issues, _active = rdd.validate_structure(
                [requirements],
                loops,
                [],
                r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$",
            )

        self.assertNotIn("invalid_loop_filename", {issue.code for issue in default_issues})
        self.assertIn("invalid_loop_filename", {issue.code for issue in strict_issues})

    def test_ready_succeeds_without_active_loop(self):
        child = semantic_entry("REQ-READ-ONLY", "Keep analysis read-only", "ROOT-REQ-TRACEABLE-LOOPS")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requirements = root / "requirements.md"
            loops = root / "loops"
            loops.mkdir()
            requirements.write_text(semantic_requirements(child), encoding="utf-8")
            (loops / "README.md").write_text("# Support\n", encoding="utf-8")
            (loops / ".notes.md").write_text("# Support\n", encoding="utf-8")

            ready_code, ready_output = self._run_main(["ready", str(requirements), "--loops", str(loops)])

        self.assertEqual(ready_code, 0)
        self.assertIn("Active loop documents: 0", ready_output)

    def test_guard_io_failure_uses_exit_code_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.md"
            loops = Path(tmp) / "loops"
            loops.mkdir()
            code, output = self._run_main(["validate", str(missing), "--loops", str(loops)])

        self.assertEqual(code, 2)
        self.assertIn("No such requirement source", output)

    def test_guard_unexpected_failure_uses_exit_code_two(self):
        with mock.patch.object(rdd, "validate_structure", side_effect=RuntimeError("unexpected guard failure")):
            code, output = self._run_main(["validate", "requirements.md"])

        self.assertEqual(code, 2)
        self.assertIn("unexpected guard failure", output)

    def test_invalid_loop_options_use_exit_code_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            requirements = Path(tmp) / "requirements.md"
            requirements.write_text(HIERARCHY_SAMPLE, encoding="utf-8")
            missing_loops_code, missing_loops_output = self._run_main(
                ["validate", str(requirements), "--loop-name-pattern", "["]
            )
            invalid_pattern_code, invalid_pattern_output = self._run_main(
                ["validate", str(requirements), "--loops", str(Path(tmp)), "--loop-name-pattern", "["]
            )

        self.assertEqual(missing_loops_code, 2)
        self.assertIn("require --loops", missing_loops_output)
        self.assertEqual(invalid_pattern_code, 2)
        self.assertIn("unterminated character set", invalid_pattern_output)

    def test_onboarding_templates_satisfy_structural_validation(self):
        project_root = Path(__file__).resolve().parents[2]
        requirements = project_root / "templates" / "requirements.md"
        loop_template = project_root / "templates" / "active_loop.md"
        with tempfile.TemporaryDirectory() as tmp:
            loops = Path(tmp) / "loops"
            loops.mkdir()
            (loops / "first-capability.md").write_text(
                loop_template.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            issues, _active = rdd.validate_structure([requirements], loops, [])

        self.assertEqual(issues, [])

    def test_existing_cli_commands_remain_successful(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text(SAMPLE, encoding="utf-8")
            results = {
                command: self._run_main([command, str(path)])[0]
                for command in ("trace", "prompt", "gaps")
            }

        self.assertEqual(results, {"trace": 0, "prompt": 0, "gaps": 0})

    def test_korean_plain_hierarchy_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.ko.md"
            path.write_text(KOREAN_HIERARCHY_SAMPLE, encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(
            trace["fields"]["root_goal"][0]["text"],
            "실행 가능한 작업이 있을 때만 Codex를 호출한다.",
        )
        self.assertEqual(len(trace["fields"]["requirement"]), 2)
        self.assertEqual(
            trace["fields"]["rationale"][0]["text"],
            "반복 polling에서 불필요한 토큰 사용을 줄여야 한다.",
        )
        self.assertEqual(
            trace["fields"]["failure_prevented"][0]["text"],
            "대기 작업이 없는데도 Codex를 호출하는 상태.",
        )
        self.assertEqual(trace["fields"]["spec"][0]["text"], "pause, cooldown, dependency gate를 먼저 평가한다.")
        self.assertEqual(trace["fields"]["revisit_when"][0]["text"], "실행 모델이 바뀔 때.")

    def test_retroactive_review_output_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "retroactive.md"
            path.write_text(RETROACTIVE_REVIEW_SAMPLE, encoding="utf-8")
            trace = rdd.build_trace(path)

        root_goals = [item["text"] for item in trace["fields"]["root_goal"]]
        requirements = [item["text"] for item in trace["fields"]["requirement"]]
        rationales = [item["text"] for item in trace["fields"]["rationale"]]
        failures = [item["text"] for item in trace["fields"]["failure_prevented"]]
        specs = [item["text"] for item in trace["fields"]["spec"]]
        review_focus = [item["text"] for item in trace["fields"]["review_focus"]]
        automation = [item["text"] for item in trace["fields"]["automation_boundary"]]
        decision_classes = [item["text"] for item in trace["fields"]["decision_class"]]
        acceptance_scopes = [item["text"] for item in trace["fields"]["acceptance_scope"]]
        promotion_rules = [item["text"] for item in trace["fields"]["promotion_rule"]]

        self.assertIn("Adopt RDD without rewriting existing project history.", root_goals)
        self.assertIn("Accept/apply output must agree with persisted task state.", requirements)
        self.assertIn("Operators decide whether to retry or clean up from this output.", rationales)
        self.assertIn("A successful mutation appearing as a lock failure.", failures)
        self.assertIn("idempotent already-applied accept returns success.", specs)
        self.assertIn("Temporary Experiment Policy.", decision_classes)
        self.assertIn("beta-only policy accepted.", acceptance_scopes)
        self.assertIn("Promote only if repeated across markets or providers.", promotion_rules)
        self.assertTrue(any("review/apply safety behavior." in text for text in review_focus))
        self.assertTrue(any("read-only review bundle generation." in text for text in automation))
        self.assertEqual(trace["fields"]["non_goals"][0]["text"], "- Do not rewrite historical task logs.")

    def test_existing_project_with_trace_gaps_recommends_retroactive_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "SPEC.md").write_text(
                "# Spec\n\nThe current CLI lists sessions.\n",
                encoding="utf-8",
            )
            (docs / "ROADMAP.md").write_text(
                "# Roadmap\n\n- Add notifications later.\n",
                encoding="utf-8",
            )

            trace = rdd.build_trace(root)
            rendered = rdd.render_gaps_markdown(trace)

        self.assertEqual(trace["recommendations"][0]["kind"], "retroactive_review_recommended")
        self.assertEqual(trace["recommendations"][0]["guide"], "docs/07-retroactive-rdd-review.md")
        self.assertIn("read-only retroactive RDD coverage review", rendered)
        self.assertIn("docs/07-retroactive-rdd-review.md", rendered)

    def test_file_scan_does_not_recommend_retroactive_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SPEC.md"
            path.write_text("# Spec\n\nOne file.\n", encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(trace["recommendations"], [])

    def _entries(self, text: str) -> list[rdd.RequirementEntry]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(text, encoding="utf-8")
            return rdd.parse_requirement_entries(path)

    def _run_main(self, argv: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = rdd.main(argv)
        return code, output.getvalue()


if __name__ == "__main__":
    unittest.main()
