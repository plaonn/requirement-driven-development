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


if __name__ == "__main__":
    unittest.main()
