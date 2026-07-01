#!/usr/bin/env python3
"""Small read-only RDD trace helper.

This tool extracts explicit Requirement Driven Development sections from
Markdown files. It does not infer missing requirements or update source files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from textwrap import shorten


SCHEMA_VERSION = "rdd.trace.v1"

FIELD_LABELS = {
    "root_goal": "Root goal",
    "requirement": "Requirement",
    "rationale": "Rationale",
    "failure_prevented": "Failure prevented",
    "spec": "Spec",
    "checks": "Tests / Checks",
    "implementation": "Implementation",
    "non_goals": "Non-goals",
    "automation_boundary": "Automation boundary",
    "boundary_clarification": "Boundary clarification",
    "review_focus": "Review focus",
    "requirement_changes": "Requirement changes discovered",
}

SECTION_ALIASES = {
    "root goal": "root_goal",
    "root goals": "root_goal",
    "근본 목표": "root_goal",
    "상위 목표": "root_goal",
    "목표": "root_goal",
    "goal": "root_goal",
    "goals": "root_goal",
    "requirement": "requirement",
    "requirements": "requirement",
    "candidate requirement": "requirement",
    "candidate requirements": "requirement",
    "요구사항": "requirement",
    "rationale": "rationale",
    "why this matters": "rationale",
    "why this exists": "rationale",
    "근거": "rationale",
    "이유": "rationale",
    "필요성": "rationale",
    "failure prevented": "failure_prevented",
    "failures prevented": "failure_prevented",
    "risk prevented": "failure_prevented",
    "risk": "failure_prevented",
    "risks": "failure_prevented",
    "예방하는 실패": "failure_prevented",
    "실패 방지": "failure_prevented",
    "방지하는 위험": "failure_prevented",
    "위험": "failure_prevented",
    "spec": "spec",
    "specs": "spec",
    "specification": "spec",
    "acceptance criteria": "spec",
    "명세": "spec",
    "규칙": "spec",
    "인수 기준": "spec",
    "tests": "checks",
    "test": "checks",
    "checks": "checks",
    "tests checks": "checks",
    "tests / checks": "checks",
    "tests/checks": "checks",
    "테스트": "checks",
    "검사": "checks",
    "테스트 검사": "checks",
    "implementation": "implementation",
    "implementation notes": "implementation",
    "implementation note": "implementation",
    "what changed": "implementation",
    "구현": "implementation",
    "구현 메모": "implementation",
    "변경 내용": "implementation",
    "non goals": "non_goals",
    "non-goals": "non_goals",
    "non goal": "non_goals",
    "non-goal": "non_goals",
    "out of scope": "non_goals",
    "비목표": "non_goals",
    "범위 밖": "non_goals",
    "제외 항목": "non_goals",
    "automation boundary": "automation_boundary",
    "자동화 경계": "automation_boundary",
    "boundary clarification": "boundary_clarification",
    "boundary clarification questions": "boundary_clarification",
    "경계 확인": "boundary_clarification",
    "경계 명확화": "boundary_clarification",
    "경계 확인 질문": "boundary_clarification",
    "review focus": "review_focus",
    "리뷰 초점": "review_focus",
    "requirement changes discovered": "requirement_changes",
    "requirement change examples": "requirement_changes",
    "what would count as requirement change": "requirement_changes",
    "발견된 요구사항 변경": "requirement_changes",
    "요구사항 변경 예시": "requirement_changes",
    "follow ups": "requirement_changes",
    "follow-ups": "requirement_changes",
    "후속 작업": "requirement_changes",
}

REQUIRED_FIELDS = (
    "root_goal",
    "requirement",
    "rationale",
    "failure_prevented",
    "spec",
    "checks",
    "non_goals",
)

CONDITIONAL_FIELDS = (
    "automation_boundary",
)

GAP_QUESTIONS = {
    "root_goal": "What larger user, product, business, technical, or operational goal does this loop serve?",
    "requirement": "What stable requirement defines this loop boundary?",
    "rationale": "Why does this requirement matter now?",
    "failure_prevented": "What bad outcome, regression, or scope failure does this requirement prevent?",
    "spec": "What rules, boundaries, contracts, or acceptance criteria express the requirement?",
    "checks": "What tests, builds, reviews, or manual checks protect the spec?",
    "non_goals": "What adjacent work is intentionally out of scope for this loop?",
    "automation_boundary": "If this loop automates state-changing work, what may run now, what needs human review, and what must not be automated yet?",
}

SKIP_DIRS = {".git", ".hg", ".svn", ".mypy_cache", ".pytest_cache", "__pycache__", "node_modules"}


@dataclass
class Section:
    field: str
    file: str
    heading: str
    level: int
    text: str


def normalize_heading(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"^#+\s*", "", lowered)
    lowered = re.sub(r"\s+#*$", "", lowered)
    lowered = re.sub(r"^\d+[\.)]\s*", "", lowered)
    lowered = lowered.replace("_", " ")
    lowered = lowered.replace(":", " ")
    lowered = re.sub(r"[`*()[\]{}]", "", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def heading_to_field(heading: str) -> str | None:
    normalized = normalize_heading(heading)
    if normalized in SECTION_ALIASES:
        return SECTION_ALIASES[normalized]
    return None


def is_fence(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def parse_markdown(path: Path, root: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings: list[tuple[int, int, str, str | None]] = []
    sections: list[Section] = []
    in_fence = False

    for index, line in enumerate(lines):
        if is_fence(line):
            in_fence = not in_fence
            continue

        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match and not in_fence:
            level = len(match.group(1))
            heading = match.group(2).strip()
            headings.append((index, level, heading, heading_to_field(heading)))

    for heading_index, (start, level, heading, field) in enumerate(headings):
        if not field:
            continue
        end = len(lines)
        for next_start, next_level, _next_heading, _next_field in headings[heading_index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        body = "\n".join(lines[start + 1 : end]).strip()
        if body:
            sections.append(
                Section(
                    field=field,
                    file=str(path.relative_to(root)),
                    heading=heading,
                    level=level,
                    text=body,
                )
            )
    return sections


def path_mentions_private(path: Path) -> bool:
    return ".private" in path.parts


def collect_markdown_paths(source: Path) -> list[Path]:
    source = source.resolve()
    allow_private = path_mentions_private(source)

    if source.is_file():
        return [source] if source.suffix.lower() == ".md" else []
    if not source.is_dir():
        raise FileNotFoundError(f"No such file or directory: {source}")

    paths: list[Path] = []
    for candidate in source.rglob("*.md"):
        parts = set(candidate.relative_to(source).parts)
        if not allow_private and ".private" in parts:
            continue
        if parts & SKIP_DIRS:
            continue
        paths.append(candidate)
    return sorted(paths)


def build_trace(source: Path) -> dict:
    root = source.resolve() if source.is_dir() else source.resolve().parent
    files = collect_markdown_paths(source)
    fields: dict[str, list[Section]] = {key: [] for key in FIELD_LABELS}
    for path in files:
        for section in parse_markdown(path, root):
            fields.setdefault(section.field, []).append(section)

    field_data = {
        key: [asdict(section) for section in sections]
        for key, sections in fields.items()
        if sections
    }
    gaps = gap_items(fields)
    return {
        "schema_version": SCHEMA_VERSION,
        "source": str(source),
        "files": [str(path.relative_to(root)) for path in files],
        "fields": field_data,
        "gaps": gaps,
        "boundary_questions": [gap["question"] for gap in gaps],
    }


def gap_items(fields: dict[str, list[Section]]) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            gaps.append(
                {
                    "field": field,
                    "label": FIELD_LABELS[field],
                    "kind": "missing",
                    "question": GAP_QUESTIONS[field],
                }
            )
    for field in CONDITIONAL_FIELDS:
        if not fields.get(field):
            gaps.append(
                {
                    "field": field,
                    "label": FIELD_LABELS[field],
                    "kind": "conditional",
                    "question": GAP_QUESTIONS[field],
                }
            )
    return gaps


def render_section_items(items: list[dict], max_items: int, max_chars: int) -> str:
    rendered: list[str] = []
    for item in items[:max_items]:
        text = shorten(item["text"].replace("\n", " "), width=max_chars, placeholder=" ...")
        rendered.append(f"- `{item['file']}` / {item['heading']}: {text}")
    if len(items) > max_items:
        rendered.append(f"- ... {len(items) - max_items} more")
    return "\n".join(rendered)


def render_trace_markdown(trace: dict, max_items: int, max_chars: int) -> str:
    lines = [
        "# RDD Compact Trace",
        "",
        f"Source: `{trace['source']}`",
        f"Files scanned: {len(trace['files'])}",
        "",
    ]
    fields: dict = trace["fields"]
    for field, label in FIELD_LABELS.items():
        if field not in fields:
            continue
        lines.extend([f"## {label}", render_section_items(fields[field], max_items, max_chars), ""])
    lines.extend(render_gap_markdown(trace))
    return "\n".join(lines).rstrip() + "\n"


def render_gap_markdown(trace: dict) -> list[str]:
    gaps = trace["gaps"]
    if not gaps:
        return ["## Boundary clarification", "No required trace gaps found.", ""]
    lines = ["## Boundary clarification needed"]
    for gap in gaps:
        label = gap["label"]
        kind = gap["kind"]
        question = gap["question"]
        prefix = "Conditional" if kind == "conditional" else "Missing"
        lines.append(f"- {prefix}: {label} - {question}")
    lines.append("")
    return lines


def render_gaps_markdown(trace: dict) -> str:
    lines = ["# RDD Trace Gaps", "", f"Source: `{trace['source']}`", ""]
    lines.extend(render_gap_markdown(trace))
    return "\n".join(lines).rstrip() + "\n"


def first_text(trace: dict, field: str, max_chars: int) -> str:
    items = trace["fields"].get(field, [])
    if not items:
        return f"[Missing] {GAP_QUESTIONS.get(field, 'Clarify this field.')}"
    chunks = []
    for item in items[:3]:
        text = shorten(item["text"].replace("\n", " "), width=max_chars, placeholder=" ...")
        chunks.append(f"- {text}")
    return "\n".join(chunks)


def render_prompt_markdown(trace: dict, max_chars: int) -> str:
    fields = (
        ("Root goal", "root_goal"),
        ("Requirement", "requirement"),
        ("Rationale", "rationale"),
        ("Failure prevented", "failure_prevented"),
        ("Spec", "spec"),
        ("Tests / Checks", "checks"),
        ("Non-goals", "non_goals"),
        ("Automation boundary", "automation_boundary"),
    )
    lines = [
        "# RDD Coding Prompt",
        "",
        "Work on this task as a requirement-driven loop.",
        "",
    ]
    for label, field in fields:
        lines.extend([f"## {label}", first_text(trace, field, max_chars), ""])
    lines.extend(
        [
            "## Instructions",
            "- Keep the requirement stable for this loop.",
            "- Refine specs and tests only when they still express the same requirement.",
            "- If the root goal, rationale, failure prevented, or automation boundary is unclear, ask boundary clarification questions before implementation.",
            "- Do not treat implementation choices as requirements unless their rationale is explicit.",
            "- Preserve non-goals and report requirement changes before expanding scope.",
            "",
            "## Final trace",
            "Summarize: Requirement -> Spec -> Tests/Checks -> Implementation",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def emit_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_trace(args: argparse.Namespace) -> int:
    trace = build_trace(args.path)
    if args.json:
        emit_json(trace)
    else:
        print(render_trace_markdown(trace, args.max_items, args.max_chars), end="")
    return 0


def command_gaps(args: argparse.Namespace) -> int:
    trace = build_trace(args.path)
    if args.json:
        emit_json(
            {
                "schema_version": trace["schema_version"],
                "source": trace["source"],
                "gaps": trace["gaps"],
                "boundary_questions": trace["boundary_questions"],
            }
        )
    else:
        print(render_gaps_markdown(trace), end="")
    return 0


def command_prompt(args: argparse.Namespace) -> int:
    trace = build_trace(args.path)
    prompt = render_prompt_markdown(trace, args.max_chars)
    if args.json:
        emit_json(
            {
                "schema_version": trace["schema_version"],
                "source": trace["source"],
                "prompt": prompt,
                "trace": trace,
            }
        )
    else:
        print(prompt, end="")
    return 0


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", type=Path, help="Markdown file or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--max-items", type=int, default=5, help="Maximum sections per field in Markdown output.")
    parser.add_argument("--max-chars", type=int, default=700, help="Maximum characters per extracted section preview.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only RDD trace extraction helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    trace = subparsers.add_parser("trace", help="Extract a compact RDD trace.")
    add_common_options(trace)
    trace.set_defaults(func=command_trace)

    prompt = subparsers.add_parser("prompt", help="Build a compact RDD coding prompt.")
    add_common_options(prompt)
    prompt.set_defaults(func=command_prompt)

    gaps = subparsers.add_parser("gaps", help="Report missing RDD trace fields.")
    add_common_options(gaps)
    gaps.set_defaults(func=command_gaps)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except OSError as exc:
        print(f"rdd: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
