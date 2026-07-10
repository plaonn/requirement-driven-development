#!/usr/bin/env python3
"""Check structural parity between canonical English and Korean companion docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPANION_ONLY_START = "<!-- companion-only:start -->"
COMPANION_ONLY_END = "<!-- companion-only:end -->"


@dataclass(frozen=True)
class Signature:
    heading_levels: tuple[int, ...]
    fenced_blocks: int
    tables: int


def document_pairs() -> list[tuple[Path, Path]]:
    pairs = [(ROOT / "README.md", ROOT / "README.ko.md")]
    pairs.extend(
        (path, ROOT / "docs" / "ko" / path.name)
        for path in sorted((ROOT / "docs").glob("*.md"))
    )
    pairs.extend(
        (path, path.with_name(f"{path.stem}.ko.md"))
        for path in sorted((ROOT / "templates").glob("*.md"))
        if not path.name.endswith(".ko.md")
    )
    pairs.extend(
        (path, ROOT / "examples" / "ko" / path.name)
        for path in sorted((ROOT / "examples").glob("*.md"))
    )
    return pairs


def structural_signature(path: Path, *, allow_companion_only: bool) -> Signature:
    heading_levels: list[int] = []
    fenced_blocks = 0
    tables = 0
    in_fence = False
    in_companion_only = False

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line == COMPANION_ONLY_START:
            if not allow_companion_only or in_companion_only:
                raise ValueError(f"{path}:{line_number}: invalid companion-only start")
            in_companion_only = True
            continue
        if line == COMPANION_ONLY_END:
            if not allow_companion_only or not in_companion_only:
                raise ValueError(f"{path}:{line_number}: unmatched companion-only end")
            in_companion_only = False
            continue
        if in_companion_only:
            continue
        if line.startswith("```"):
            in_fence = not in_fence
            if in_fence:
                fenced_blocks += 1
            continue
        if in_fence:
            continue
        if line.startswith("#") and line.lstrip("#").startswith(" "):
            heading_levels.append(len(line) - len(line.lstrip("#")))
        if line.startswith("| ---"):
            tables += 1

    if in_companion_only:
        raise ValueError(f"{path}: unclosed companion-only section")
    if in_fence:
        raise ValueError(f"{path}: unclosed fenced code block")

    return Signature(tuple(heading_levels), fenced_blocks, tables)


def main() -> int:
    errors: list[str] = []

    for canonical, companion in document_pairs():
        if not companion.exists():
            errors.append(f"missing companion: {companion.relative_to(ROOT)}")
            continue
        try:
            canonical_signature = structural_signature(
                canonical, allow_companion_only=False
            )
            companion_signature = structural_signature(
                companion, allow_companion_only=True
            )
        except ValueError as error:
            errors.append(str(error))
            continue
        if canonical_signature != companion_signature:
            errors.append(
                f"structural drift: {canonical.relative_to(ROOT)} != "
                f"{companion.relative_to(ROOT)}\n"
                f"  canonical: {canonical_signature}\n"
                f"  companion: {companion_signature}"
            )

    if errors:
        print("Companion documentation check failed:\n")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("Companion documentation structure is aligned.")
    print("Manual semantic-equivalence review is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
