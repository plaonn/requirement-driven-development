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
    "need": "Need",
    "requirement": "Requirement",
    "validity_scope": "Requirement validity",
    "rationale": "Rationale",
    "failure_prevented": "Failure prevented",
    "assumptions": "Assumptions",
    "revisit_when": "Revisit when",
    "revisit_signal_status": "Revisit signal status",
    "spec": "Spec",
    "checks": "Tests / Checks",
    "implementation": "Implementation",
    "non_goals": "Non-goals",
    "automation_boundary": "Automation boundary",
    "decision_class": "Decision class",
    "durability": "Durability",
    "acceptance_scope": "Acceptance scope",
    "policy_horizon": "Policy horizon",
    "promotion_rule": "Promotion rule",
    "expiration_rule": "Expiration rule",
    "canonical_owner": "Canonical owner",
    "boundary_clarification": "Boundary clarification",
    "review_focus": "Review focus",
    "requirement_changes": "Requirement changes discovered",
    "revalidation_outcome": "Revalidation outcome",
    "affected_traces": "Affected traces",
}

SECTION_ALIASES = {
    "root goal": "root_goal",
    "root goals": "root_goal",
    "근본 목표": "root_goal",
    "상위 목표": "root_goal",
    "목표": "root_goal",
    "goal": "root_goal",
    "goals": "root_goal",
    "need": "need",
    "needs": "need",
    "stakeholder need": "need",
    "stakeholder needs": "need",
    "need context": "need",
    "need / goal context": "need",
    "need goal context": "need",
    "stakeholder 필요": "need",
    "need 맥락": "need",
    "필요 맥락": "need",
    "requirement": "requirement",
    "candidate requirement": "requirement",
    "candidate requirements": "requirement",
    "요구사항": "requirement",
    "복원된 requirement": "requirement",
    "requirement validity": "validity_scope",
    "validity scope": "validity_scope",
    "validity": "validity_scope",
    "유효성 범위": "validity_scope",
    "requirement 유효성": "validity_scope",
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
    "방지 실패": "failure_prevented",
    "예방하는 실패": "failure_prevented",
    "실패 방지": "failure_prevented",
    "실패 예방": "failure_prevented",
    "방지하는 위험": "failure_prevented",
    "위험": "failure_prevented",
    "spec": "spec",
    "specs": "spec",
    "specification": "spec",
    "acceptance criteria": "spec",
    "derived spec": "spec",
    "derived specs": "spec",
    "derived specs tests": "spec",
    "derived specs/tests": "spec",
    "spec trace": "spec",
    "명세": "spec",
    "규칙": "spec",
    "인수 기준": "spec",
    "파생 규칙": "spec",
    "파생 명세": "spec",
    "파생 specs tests": "spec",
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
    "implementation choices": "implementation",
    "구현": "implementation",
    "구현 메모": "implementation",
    "변경 내용": "implementation",
    "구현 선택": "implementation",
    "구현 선택지": "implementation",
    "non goals": "non_goals",
    "non-goals": "non_goals",
    "non goal": "non_goals",
    "non-goal": "non_goals",
    "out of scope": "non_goals",
    "비목표": "non_goals",
    "범위 밖": "non_goals",
    "제외 항목": "non_goals",
    "automation boundary": "automation_boundary",
    "automate now": "automation_boundary",
    "require human review": "automation_boundary",
    "require review": "automation_boundary",
    "do not automate yet": "automation_boundary",
    "자동화 경계": "automation_boundary",
    "지금 자동화": "automation_boundary",
    "사람 리뷰 필요": "automation_boundary",
    "리뷰 필요": "automation_boundary",
    "아직 자동화하지 않음": "automation_boundary",
    "decision class": "decision_class",
    "decision classification": "decision_class",
    "decision register": "decision_class",
    "durability": "durability",
    "acceptance scope": "acceptance_scope",
    "accepted scope": "acceptance_scope",
    "policy horizon": "policy_horizon",
    "promotion rule": "promotion_rule",
    "expiration rule": "expiration_rule",
    "canonical owner": "canonical_owner",
    "결정 분류": "decision_class",
    "분류": "decision_class",
    "지속성": "durability",
    "수용 범위": "acceptance_scope",
    "승인 범위": "acceptance_scope",
    "정책 horizon": "policy_horizon",
    "정책 기간": "policy_horizon",
    "승격 규칙": "promotion_rule",
    "만료 규칙": "expiration_rule",
    "기준 owner": "canonical_owner",
    "소유자": "canonical_owner",
    "boundary clarification": "boundary_clarification",
    "boundary clarification questions": "boundary_clarification",
    "boundary questions first": "boundary_clarification",
    "open questions": "boundary_clarification",
    "unresolved requirement candidates": "boundary_clarification",
    "question needed": "boundary_clarification",
    "adoption boundary": "boundary_clarification",
    "경계 확인": "boundary_clarification",
    "경계 명확화": "boundary_clarification",
    "경계 확인 질문": "boundary_clarification",
    "열린 질문": "boundary_clarification",
    "미해결 requirement 후보": "boundary_clarification",
    "미해결 요구사항 후보": "boundary_clarification",
    "필요한 질문": "boundary_clarification",
    "승격 경계": "boundary_clarification",
    "review focus": "review_focus",
    "retroactive coverage": "review_focus",
    "change risk": "review_focus",
    "evidence": "review_focus",
    "known trace": "review_focus",
    "리뷰 초점": "review_focus",
    "소급 coverage": "review_focus",
    "소급 커버리지": "review_focus",
    "변경 위험": "review_focus",
    "근거 문서": "review_focus",
    "확인된 trace": "review_focus",
    "requirement changes discovered": "requirement_changes",
    "requirement change examples": "requirement_changes",
    "what would count as requirement change": "requirement_changes",
    "발견된 요구사항 변경": "requirement_changes",
    "요구사항 변경 예시": "requirement_changes",
    "follow ups": "requirement_changes",
    "follow-ups": "requirement_changes",
    "후속 작업": "requirement_changes",
    "revalidation outcome": "revalidation_outcome",
    "revalidation result": "revalidation_outcome",
    "disposition": "revalidation_outcome",
    "재검증 결과": "revalidation_outcome",
    "처분": "revalidation_outcome",
    "affected traces": "affected_traces",
    "affected trace": "affected_traces",
    "propagation": "affected_traces",
    "영향받는 trace": "affected_traces",
    "전파": "affected_traces",
    "assumption": "assumptions",
    "assumptions": "assumptions",
    "가정": "assumptions",
    "revisit": "revisit_when",
    "revisit when": "revisit_when",
    "재검토 조건": "revisit_when",
    "재검토 시점": "revisit_when",
    "다시 볼 때": "revisit_when",
    "revisit signal status": "revisit_signal_status",
    "revisit status": "revisit_signal_status",
    "재검토 신호 상태": "revisit_signal_status",
}

REQUIRED_FIELDS = (
    "root_goal",
    "requirement",
    "validity_scope",
    "rationale",
    "failure_prevented",
    "spec",
    "checks",
    "non_goals",
)

CONDITIONAL_FIELDS = (
    "automation_boundary",
)

CURRENT_TRUTH_FILENAMES = {
    "readme.md",
    "readme.ko.md",
    "spec.md",
    "roadmap.md",
    "tasks.md",
}

GAP_QUESTIONS = {
    "root_goal": "What larger user, product, business, technical, or operational goal does this loop serve?",
    "requirement": "What stable requirement defines this loop boundary?",
    "validity_scope": "Is this a loop-local requirement, durable requirement, or temporary/scoped policy?",
    "rationale": "Why does this requirement matter now?",
    "failure_prevented": "What bad outcome, regression, or scope failure does this requirement prevent?",
    "spec": "What rules, boundaries, contracts, or acceptance criteria express the requirement?",
    "checks": "What tests, builds, reviews, or manual checks protect the spec?",
    "non_goals": "What adjacent work is intentionally out of scope for this loop?",
    "automation_boundary": "If this loop automates state-changing work, what may run now, what needs human review, and what must not be automated yet?",
    "assumptions": "What conditions must remain true for this durable requirement to stay valid?",
    "revisit_when": "What observable signals should trigger revalidation of this durable requirement?",
    "expiration_rule": "What event or condition expires this temporary or scoped policy?",
}

SKIP_DIRS = {".git", ".hg", ".svn", ".mypy_cache", ".pytest_cache", "__pycache__", "node_modules"}

NUMERIC_REQUIREMENT_RE = re.compile(r"^R(\d+)$", re.IGNORECASE)
ROOT_REQUIREMENT_RE = re.compile(r"^ROOT-REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CHILD_REQUIREMENT_RE = re.compile(r"^REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*$")

SEMANTIC_REQUIRED_FIELDS = (
    "parent",
    "decision_class",
    "validity_scope",
    "requirement",
    "rationale",
    "failure_prevented",
    "assumptions",
    "derived_specs",
    "revisit_when",
)

LOOP_REQUIRED_HEADINGS = (
    "spec",
    "checks",
    "implementation",
    "review",
    "non_goals",
)


@dataclass
class Section:
    field: str
    file: str
    heading: str
    level: int
    text: str


@dataclass
class RequirementEntry:
    key: str
    title: str
    file: str
    line: int
    fields: dict[str, str]


@dataclass
class ValidationIssue:
    code: str
    file: str
    message: str


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


def markdown_headings(lines: list[str]) -> list[tuple[int, int, str, str | None]]:
    headings: list[tuple[int, int, str, str | None]] = []
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
    return headings


def parse_markdown(path: Path, root: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines)
    sections: list[Section] = []

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


def parse_inline_field_lines(
    lines: list[str],
    *,
    allow_plain: bool,
    respect_fences: bool,
) -> list[tuple[int, str, str]]:
    parsed: list[tuple[int, str, str]] = []
    current_index: int | None = None
    in_fence = False

    prefix = r"(?:[-*]\s+)?"
    if allow_plain:
        pattern = re.compile(rf"^\s*{prefix}([^:\n]{{1,80}}):\s*(.*)$")
    else:
        pattern = re.compile(r"^\s*[-*]\s+([^:\n]{1,80}):\s*(.*)$")

    for line_number, line in enumerate(lines):
        if respect_fences and is_fence(line):
            in_fence = not in_fence
            current_index = None
            continue
        if in_fence:
            continue

        match = pattern.match(line)
        if match:
            field = heading_to_field(match.group(1))
            if field:
                parsed.append((line_number, field, match.group(2).strip()))
                current_index = len(parsed) - 1
                continue
            current_index = None
            continue

        if current_index is not None and (line.startswith("  ") or line.startswith("\t")):
            continuation = line.strip()
            if continuation:
                item_line, item_field, item_value = parsed[current_index]
                parsed[current_index] = (item_line, item_field, "\n".join(part for part in (item_value, continuation) if part))
            continue

        if line.strip():
            current_index = None

    return [(line_number, field, value) for line_number, field, value in parsed if value]


def parse_field_lines(lines: list[str], *, allow_plain: bool = True) -> dict[str, str]:
    fields: dict[str, list[str]] = {}
    for _line_number, field, value in parse_inline_field_lines(lines, allow_plain=allow_plain, respect_fences=True):
        fields.setdefault(field, []).append(value)

    return {field: "\n".join(parts).strip() for field, parts in fields.items() if parts}


def nearest_heading(headings: list[tuple[int, int, str, str | None]], line_number: int) -> tuple[int, str]:
    current_level = 0
    current_heading = "inline field"
    for heading_line, level, heading, _field in headings:
        if heading_line >= line_number:
            break
        current_level = level
        current_heading = heading
    return current_level, current_heading


def parse_inline_fields(path: Path, root: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines)
    sections: list[Section] = []

    for line_number, field, value in parse_inline_field_lines(lines, allow_plain=True, respect_fences=True):
        level, heading = nearest_heading(headings, line_number)
        sections.append(
            Section(
                field=field,
                file=str(path.relative_to(root)),
                heading=heading,
                level=level,
                text=value,
            )
        )
    return sections


def parse_rdd_hierarchy(path: Path, root: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines)
    sections: list[Section] = []

    for heading_index, (start, level, heading, _field) in enumerate(headings):
        match = re.match(r"^R(\d+)\s*:\s*(.+)$", heading.strip(), re.IGNORECASE)
        if not match:
            continue

        requirement_number = int(match.group(1))
        title = match.group(2).strip()
        end = len(lines)
        for next_start, next_level, _next_heading, _next_field in headings[heading_index + 1 :]:
            if next_level <= level:
                end = next_start
                break

        bullet_fields = parse_field_lines(lines[start + 1 : end], allow_plain=True)
        heading_label = heading.strip()

        if requirement_number == 0:
            sections.append(
                Section(
                    field="root_goal",
                    file=str(path.relative_to(root)),
                    heading=heading_label,
                    level=level,
                    text=bullet_fields.get("requirement") or title,
                )
            )

        for field, value in bullet_fields.items():
            sections.append(
                Section(
                    field=field,
                    file=str(path.relative_to(root)),
                    heading=heading_label,
                    level=level,
                    text=value,
                )
            )

    return sections


def semantic_heading_parts(heading: str) -> tuple[str, str] | None:
    match = re.match(r"^(ROOT-REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*|REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*)\s*:\s*(.+)$", heading)
    if not match:
        return None
    return match.group(1), match.group(2).strip()


def parse_semantic_hierarchy(path: Path, root: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines)
    sections: list[Section] = []

    for heading_index, (start, level, heading, _field) in enumerate(headings):
        parts = semantic_heading_parts(heading.strip())
        if not parts:
            continue

        _key, title = parts
        end = len(lines)
        for next_start, next_level, _next_heading, _next_field in headings[heading_index + 1 :]:
            if next_level <= level:
                end = next_start
                break

        bullet_fields = parse_field_lines(lines[start + 1 : end], allow_plain=True)
        heading_label = heading.strip()
        requirement_text = bullet_fields.get("requirement") or title
        sections.append(
            Section(
                field="requirement",
                file=str(path.relative_to(root)),
                heading=heading_label,
                level=level,
                text=requirement_text,
            )
        )

        for field, value in bullet_fields.items():
            if field == "requirement":
                continue
            sections.append(
                Section(
                    field=field,
                    file=str(path.relative_to(root)),
                    heading=heading_label,
                    level=level,
                    text=value,
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
        for section in parse_inline_fields(path, root):
            fields.setdefault(section.field, []).append(section)
        for section in parse_rdd_hierarchy(path, root):
            fields.setdefault(section.field, []).append(section)
        for section in parse_semantic_hierarchy(path, root):
            fields.setdefault(section.field, []).append(section)
    fields = dedupe_fields(fields)

    field_data = {
        key: [asdict(section) for section in sections]
        for key, sections in fields.items()
        if sections
    }
    gaps = gap_items(fields)
    recommendations = recommendation_items(source, files, fields)
    return {
        "schema_version": SCHEMA_VERSION,
        "source": str(source),
        "files": [str(path.relative_to(root)) for path in files],
        "fields": field_data,
        "gaps": gaps,
        "recommendations": recommendations,
        "boundary_questions": [gap["question"] for gap in gaps],
    }


def dedupe_fields(fields: dict[str, list[Section]]) -> dict[str, list[Section]]:
    deduped: dict[str, list[Section]] = {}
    for field, sections in fields.items():
        seen: set[tuple[str, str, str, str]] = set()
        for section in sections:
            key = (section.field, section.file, section.heading, section.text)
            if key in seen:
                continue
            seen.add(key)
            deduped.setdefault(field, []).append(section)
    return deduped


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

    validity_text = "\n".join(
        section.text.lower() for section in fields.get("validity_scope", [])
    )
    if "durable" in validity_text:
        for field in ("assumptions", "revisit_when"):
            if not fields.get(field):
                gaps.append(
                    {
                        "field": field,
                        "label": FIELD_LABELS[field],
                        "kind": "missing",
                        "question": GAP_QUESTIONS[field],
                    }
                )
    if any(term in validity_text for term in ("temporary", "scoped")):
        if not fields.get("expiration_rule"):
            gaps.append(
                {
                    "field": "expiration_rule",
                    "label": FIELD_LABELS["expiration_rule"],
                    "kind": "missing",
                    "question": GAP_QUESTIONS["expiration_rule"],
                }
            )
    return gaps


def has_current_truth_surface(files: list[Path]) -> bool:
    for path in files:
        lower_name = path.name.lower()
        lower_parts = [part.lower() for part in path.parts]
        if lower_name in CURRENT_TRUTH_FILENAMES:
            return True
        if "docs" in lower_parts and lower_name.endswith(".md"):
            return True
        if "tests" in lower_parts and lower_name.endswith(".md"):
            return True
    return False


def recommendation_items(source: Path, files: list[Path], fields: dict[str, list[Section]]) -> list[dict[str, str]]:
    if not source.is_dir():
        return []
    if not files or not has_current_truth_surface(files):
        return []

    missing_core_trace = any(
        not fields.get(field)
        for field in ("root_goal", "requirement", "rationale", "failure_prevented")
    )
    if not missing_core_trace:
        return []

    return [
        {
            "kind": "retroactive_review_recommended",
            "guide": "docs/07-retroactive-rdd-review.md",
            "message": (
                "This directory has current-truth surfaces but incomplete requirement trace. "
                "Start with a read-only retroactive RDD coverage review before promoting "
                "recovered candidates into source-of-truth docs or implementation work."
            ),
        }
    ]


def normalize_contract_label(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9가-힣]+", "_", lowered)
    return lowered.strip("_")


CONTRACT_FIELD_ALIASES = {
    "parent": "parent",
    "decision_class": "decision_class",
    "validity_scope": "validity_scope",
    "requirement_validity": "validity_scope",
    "requirement": "requirement",
    "요구사항": "requirement",
    "rationale": "rationale",
    "근거": "rationale",
    "failure_prevented": "failure_prevented",
    "실패_방지": "failure_prevented",
    "assumptions": "assumptions",
    "가정": "assumptions",
    "derived_specs": "derived_specs",
    "derived_spec": "derived_specs",
    "파생_명세": "derived_specs",
    "revisit_when": "revisit_when",
    "재검토_조건": "revisit_when",
    "previous_identifiers": "previous_identifiers",
    "previous_identifier": "previous_identifiers",
    "requirement_reference": "requirement_reference",
    "loop_unit": "loop_unit",
    "merge_unit": "loop_unit",
}


CONTRACT_HEADING_ALIASES = {
    "spec": "spec",
    "specification": "spec",
    "명세": "spec",
    "tests": "checks",
    "test": "checks",
    "checks": "checks",
    "tests_checks": "checks",
    "테스트": "checks",
    "검사": "checks",
    "implementation": "implementation",
    "구현": "implementation",
    "review": "review",
    "review_focus": "review",
    "리뷰": "review",
    "non_goals": "non_goals",
    "non_goal": "non_goals",
    "비목표": "non_goals",
}


def parse_contract_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_fence = False
    pattern = re.compile(r"^\s*(?:[-*]\s+)?([^:\n]{1,80}):\s*(.*?)\s*$")

    for line in lines:
        if is_fence(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = pattern.match(line)
        if not match:
            continue
        alias = CONTRACT_FIELD_ALIASES.get(normalize_contract_label(match.group(1)))
        value = match.group(2).strip()
        if alias and value and alias not in fields:
            fields[alias] = value
    return fields


def parse_requirement_entries(path: Path, *, display_name: str | None = None) -> list[RequirementEntry]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = markdown_headings(lines)
    entries: list[RequirementEntry] = []

    for heading_index, (start, level, heading, _field) in enumerate(headings):
        key: str | None = None
        title: str | None = None
        semantic = semantic_heading_parts(heading.strip())
        if semantic:
            key, title = semantic
        else:
            numeric = re.match(r"^(R\d+)\s*:\s*(.+)$", heading.strip(), re.IGNORECASE)
            if numeric:
                key = numeric.group(1).upper()
                title = numeric.group(2).strip()
            else:
                candidate = re.match(r"^([^:\s]+)\s*:\s*(.+)$", heading.strip())
                if candidate and candidate.group(1).upper().startswith(("ROOT-REQ", "REQ-")):
                    key = candidate.group(1)
                    title = candidate.group(2).strip()
        if not key or title is None:
            continue

        end = len(lines)
        for next_start, next_level, _next_heading, _next_field in headings[heading_index + 1 :]:
            if next_level <= level:
                end = next_start
                break
        entries.append(
            RequirementEntry(
                key=key,
                title=title,
                file=display_name or path.name,
                line=start + 1,
                fields=parse_contract_fields(lines[start + 1 : end]),
            )
        )
    return entries


def split_identifiers(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def validate_requirement_hierarchy(entries: list[RequirementEntry]) -> tuple[list[ValidationIssue], dict[str, str]]:
    issues: list[ValidationIssue] = []
    aliases: dict[str, str] = {}
    primary: dict[str, RequirementEntry] = {}
    numeric_entries = [entry for entry in entries if NUMERIC_REQUIREMENT_RE.fullmatch(entry.key)]
    semantic_entries = [
        entry
        for entry in entries
        if ROOT_REQUIREMENT_RE.fullmatch(entry.key) or CHILD_REQUIREMENT_RE.fullmatch(entry.key)
    ]

    if not entries:
        issues.append(ValidationIssue("missing_hierarchy", "", "No numeric or semantic requirement entries were found."))
        return issues, aliases

    if numeric_entries and semantic_entries:
        issues.append(
            ValidationIssue(
                "mixed_hierarchy",
                entries[0].file,
                "One source-of-truth hierarchy must not mix numeric and semantic primary identifiers.",
            )
        )

    for entry in entries:
        valid_primary = (
            NUMERIC_REQUIREMENT_RE.fullmatch(entry.key)
            or ROOT_REQUIREMENT_RE.fullmatch(entry.key)
            or CHILD_REQUIREMENT_RE.fullmatch(entry.key)
        )
        if not valid_primary:
            issues.append(
                ValidationIssue(
                    "invalid_requirement_identifier",
                    entry.file,
                    f"Invalid requirement identifier {entry.key} at line {entry.line}.",
                )
            )
        if entry.key in primary:
            issues.append(
                ValidationIssue(
                    "duplicate_key",
                    entry.file,
                    f"Duplicate requirement identifier {entry.key} at line {entry.line}.",
                )
            )
        else:
            primary[entry.key] = entry

    if numeric_entries:
        roots = [entry for entry in numeric_entries if entry.key == "R0"]
        if len(roots) != 1:
            issues.append(
                ValidationIssue(
                    "numeric_root_count",
                    numeric_entries[0].file,
                    f"Numeric hierarchy must contain exactly one R0 entry; found {len(roots)}.",
                )
            )

    if semantic_entries:
        roots = [entry for entry in semantic_entries if ROOT_REQUIREMENT_RE.fullmatch(entry.key)]
        if len(roots) != 1:
            issues.append(
                ValidationIssue(
                    "semantic_root_count",
                    semantic_entries[0].file,
                    f"Semantic hierarchy must contain exactly one ROOT-REQ-* entry; found {len(roots)}.",
                )
            )

        for entry in semantic_entries:
            for field in SEMANTIC_REQUIRED_FIELDS:
                if not entry.fields.get(field):
                    issues.append(
                        ValidationIssue(
                            "missing_required_field",
                            entry.file,
                            f"{entry.key} is missing required field {field.replace('_', ' ').title()}.",
                        )
                    )

            parent = entry.fields.get("parent", "")
            decision_class = entry.fields.get("decision_class", "").rstrip(".").lower()
            if decision_class and decision_class != "durable requirement":
                issues.append(
                    ValidationIssue(
                        "invalid_root_decision_class"
                        if ROOT_REQUIREMENT_RE.fullmatch(entry.key)
                        else "invalid_durable_decision_class",
                        entry.file,
                        f"{entry.key} must use Decision class: Durable Requirement.",
                    )
                )
            if ROOT_REQUIREMENT_RE.fullmatch(entry.key):
                if parent.lower() != "none":
                    issues.append(
                        ValidationIssue("invalid_root_parent", entry.file, f"{entry.key} must use Parent: none.")
                    )
            elif parent.lower() == "none":
                issues.append(
                    ValidationIssue("invalid_child_parent", entry.file, f"{entry.key} must reference a parent requirement.")
                )

            validity = entry.fields.get("validity_scope", "").rstrip(".").lower()
            if validity and validity not in {"durable", "durable requirement"}:
                issues.append(
                    ValidationIssue(
                        "invalid_durable_validity",
                        entry.file,
                        f"{entry.key} must use Validity scope: Durable.",
                    )
                )

    for entry in entries:
        for alias in split_identifiers(entry.fields.get("previous_identifiers", "")):
            valid_alias = (
                NUMERIC_REQUIREMENT_RE.fullmatch(alias)
                or ROOT_REQUIREMENT_RE.fullmatch(alias)
                or CHILD_REQUIREMENT_RE.fullmatch(alias)
            )
            if not valid_alias:
                issues.append(
                    ValidationIssue("invalid_previous_identifier", entry.file, f"Invalid previous identifier {alias} on {entry.key}.")
                )
                continue
            if alias in primary or alias in aliases:
                issues.append(
                    ValidationIssue("duplicate_previous_identifier", entry.file, f"Previous identifier {alias} is already in use.")
                )
                continue
            aliases[alias] = entry.key

    if semantic_entries:
        semantic_primary = {entry.key for entry in semantic_entries}
        for entry in semantic_entries:
            parent = entry.fields.get("parent", "")
            if not parent or parent.lower() == "none":
                continue
            if parent not in semantic_primary:
                issues.append(
                    ValidationIssue("missing_parent", entry.file, f"{entry.key} references undefined parent {parent}.")
                )

        graph = {
            entry.key: entry.fields.get("parent", "")
            for entry in semantic_entries
            if entry.fields.get("parent", "").lower() != "none"
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(key: str, trail: list[str]) -> None:
            if key in visited:
                return
            if key in visiting:
                cycle_start = trail.index(key) if key in trail else 0
                cycle = trail[cycle_start:] + [key]
                issues.append(
                    ValidationIssue("hierarchy_cycle", primary[key].file, f"Requirement hierarchy cycle: {' -> '.join(cycle)}.")
                )
                return
            visiting.add(key)
            parent = graph.get(key)
            if parent in graph:
                visit(parent, trail + [key])
            visiting.remove(key)
            visited.add(key)

        for key in graph:
            visit(key, [])

    return issues, aliases


def collect_active_loop_paths(loop_dir: Path, excluded: list[str]) -> list[Path]:
    if not loop_dir.is_dir():
        raise FileNotFoundError(f"No such active-loop directory: {loop_dir}")
    excluded_paths = {Path(item).as_posix().lstrip("./") for item in excluded}
    paths: list[Path] = []
    for path in sorted(candidate for candidate in loop_dir.rglob("*") if candidate.is_file()):
        if path.suffix.lower() != ".md":
            continue
        relative = path.relative_to(loop_dir)
        if path.name.lower() == "readme.md":
            continue
        if any(part.startswith(".") for part in relative.parts):
            continue
        if relative.as_posix() in excluded_paths:
            continue
        paths.append(path)
    return paths


def validate_active_loops(
    loop_dir: Path,
    loop_paths: list[Path],
    valid_identifiers: set[str],
    loop_name_pattern: re.Pattern[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path in loop_paths:
        relative = path.relative_to(loop_dir).as_posix()
        if loop_name_pattern and not loop_name_pattern.fullmatch(path.name):
            issues.append(
                ValidationIssue(
                    "invalid_loop_filename",
                    relative,
                    f"Loop filename does not match configured pattern {loop_name_pattern.pattern}.",
                )
            )

        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        fields = parse_contract_fields(lines)
        reference = fields.get("requirement_reference")
        if not reference:
            issues.append(
                ValidationIssue("missing_loop_metadata", relative, "Loop is missing Requirement reference metadata.")
            )
        elif reference not in valid_identifiers:
            issues.append(
                ValidationIssue(
                    "undefined_requirement_reference",
                    relative,
                    f"Loop references undefined requirement {reference}.",
                )
            )
        if not fields.get("loop_unit"):
            issues.append(ValidationIssue("missing_loop_metadata", relative, "Loop is missing Loop unit metadata."))

        present_headings = {
            CONTRACT_HEADING_ALIASES.get(normalize_contract_label(heading))
            for _line, _level, heading, _field in markdown_headings(lines)
        }
        for required in LOOP_REQUIRED_HEADINGS:
            if required not in present_headings:
                issues.append(
                    ValidationIssue(
                        "missing_loop_section",
                        relative,
                        f"Loop is missing required {required.replace('_', ' ').title()} section.",
                    )
                )
    return issues


def collect_requirement_source_paths(sources: list[Path]) -> list[Path]:
    paths: dict[Path, Path] = {}
    for source in sources:
        if source.is_file():
            if source.suffix.lower() != ".md":
                raise ValueError(f"Requirement source must be Markdown: {source}")
            paths[source.resolve()] = source
            continue
        if not source.is_dir():
            raise FileNotFoundError(f"No such requirement source: {source}")
        for candidate in sorted(source.rglob("*")):
            if not candidate.is_file() or candidate.suffix.lower() != ".md":
                continue
            relative = candidate.relative_to(source)
            if candidate.name.lower() == "readme.md":
                continue
            if any(part.startswith(".") for part in relative.parts):
                continue
            paths[candidate.resolve()] = candidate
    return [paths[key] for key in sorted(paths, key=lambda item: item.as_posix())]


def validate_structure(
    requirement_sources: list[Path],
    loop_dir: Path | None,
    excluded: list[str],
    loop_name_pattern: str | None = None,
) -> tuple[list[ValidationIssue], list[Path]]:
    if loop_dir is None and (excluded or loop_name_pattern):
        raise ValueError("Loop exclusion and filename options require --loops.")
    source_paths = collect_requirement_source_paths(requirement_sources)
    entries = [
        entry
        for path in source_paths
        for entry in parse_requirement_entries(path, display_name=path.as_posix())
    ]
    issues, _aliases = validate_requirement_hierarchy(entries)
    if loop_dir is None:
        return issues, []
    loop_paths = collect_active_loop_paths(loop_dir, excluded)
    valid_identifiers = {entry.key for entry in entries}
    compiled_pattern = re.compile(loop_name_pattern) if loop_name_pattern else None
    issues.extend(validate_active_loops(loop_dir, loop_paths, valid_identifiers, compiled_pattern))
    return issues, loop_paths


def render_validation_result(
    command: str,
    issues: list[ValidationIssue],
    active_loops: list[Path],
    loop_dir: Path | None,
) -> str:
    lines = [f"# RDD {command.title()}", ""]
    if issues:
        lines.append("Structural contract violations:")
        for issue in issues:
            location = f"{issue.file}: " if issue.file else ""
            lines.append(f"- [{issue.code}] {location}{issue.message}")
    else:
        lines.append("No structural contract violations found.")
    if loop_dir is None:
        lines.extend(["", "Active loop validation: not requested."])
    else:
        lines.extend(["", f"Active loop documents: {len(active_loops)}"])
    if active_loops and loop_dir is not None:
        lines.extend(f"- {path.relative_to(loop_dir).as_posix()}" for path in active_loops)
    return "\n".join(lines).rstrip() + "\n"


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


def render_recommendation_markdown(trace: dict) -> list[str]:
    recommendations = trace.get("recommendations", [])
    if not recommendations:
        return []

    lines = ["## RDD review recommendations"]
    for item in recommendations:
        lines.append(f"- {item['message']} Guide: `{item['guide']}`")
    lines.append("")
    return lines


def render_gaps_markdown(trace: dict) -> str:
    lines = ["# RDD Trace Gaps", "", f"Source: `{trace['source']}`", ""]
    lines.extend(render_gap_markdown(trace))
    lines.extend(render_recommendation_markdown(trace))
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
                "recommendations": trace["recommendations"],
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


def command_validate(args: argparse.Namespace) -> int:
    issues, active_loops = validate_structure(
        args.paths,
        args.loops,
        args.exclude_loop,
        args.loop_name_pattern,
    )
    print(render_validation_result("validate", issues, active_loops, args.loops), end="")
    return 1 if issues else 0


def command_ready(args: argparse.Namespace) -> int:
    issues, active_loops = validate_structure(
        args.paths,
        args.loops,
        args.exclude_loop,
        args.loop_name_pattern,
    )
    for path in active_loops:
        issues.append(
            ValidationIssue(
                "active_loop_remaining",
                path.relative_to(args.loops).as_posix(),
                "Ready requires the configured active-loop directory to contain no loop documents.",
            )
        )
    print(render_validation_result("ready", issues, active_loops, args.loops), end="")
    return 1 if issues else 0


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", type=Path, help="Markdown file or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--max-items", type=int, default=5, help="Maximum sections per field in Markdown output.")
    parser.add_argument("--max-chars", type=int, default=700, help="Maximum characters per extracted section preview.")


def add_guard_options(parser: argparse.ArgumentParser, *, loops_required: bool) -> None:
    parser.add_argument(
        "paths",
        type=Path,
        nargs="+",
        help="One or more source-of-truth requirement Markdown files or directories.",
    )
    parser.add_argument(
        "--loops",
        type=Path,
        required=loops_required,
        help="Configured active-loop directory.",
    )
    parser.add_argument(
        "--exclude-loop",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help="Support file to exclude relative to the active-loop directory; repeat as needed.",
    )
    parser.add_argument(
        "--loop-name-pattern",
        help="Optional regular expression that every active-loop filename must match.",
    )


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

    validate = subparsers.add_parser("validate", help="Validate requirement hierarchy and active-loop structure.")
    add_guard_options(validate, loops_required=False)
    validate.set_defaults(func=command_validate)

    ready = subparsers.add_parser("ready", help="Validate structure and require no active loop documents.")
    add_guard_options(ready, loops_required=True)
    ready.set_defaults(func=command_ready)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except OSError as exc:
        print(f"rdd: {exc}", file=sys.stderr)
        return 2 if args.command in {"validate", "ready"} else 1
    except UnicodeError as exc:
        if args.command not in {"validate", "ready"}:
            raise
        print(f"rdd: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        if args.command not in {"validate", "ready"}:
            raise
        print(f"rdd: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
