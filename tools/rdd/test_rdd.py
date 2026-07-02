#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

import rdd


SAMPLE = """# Example

```text
# Requirement
This heading is inside a fence and should be ignored.
```

## Root goal
Keep development loops traceable.

## Requirement
Extract explicit trace sections.

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
  Derived specs/tests: idempotent already-applied accept returns success.
  Revisit when: accept/apply state transitions are redesigned.

## Automation Boundary

- Automate now: read-only review bundle generation.
- Require human review: source-of-truth requirement adoption.
- Do not automate yet: broad policy changes.

## Non-goals

- Do not rewrite historical task logs.
"""


class RddToolTest(unittest.TestCase):
    def test_trace_extracts_expected_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text(SAMPLE, encoding="utf-8")
            trace = rdd.build_trace(path)

        self.assertEqual(trace["schema_version"], "rdd.trace.v1")
        self.assertIn("requirement", trace["fields"])
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
        self.assertIn("automation_boundary", gap_fields)

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

        self.assertIn("Adopt RDD without rewriting existing project history.", root_goals)
        self.assertIn("Accept/apply output must agree with persisted task state.", requirements)
        self.assertIn("Operators decide whether to retry or clean up from this output.", rationales)
        self.assertIn("A successful mutation appearing as a lock failure.", failures)
        self.assertIn("idempotent already-applied accept returns success.", specs)
        self.assertTrue(any("review/apply safety behavior." in text for text in review_focus))
        self.assertTrue(any("read-only review bundle generation." in text for text in automation))
        self.assertEqual(trace["fields"]["non_goals"][0]["text"], "- Do not rewrite historical task logs.")


if __name__ == "__main__":
    unittest.main()
