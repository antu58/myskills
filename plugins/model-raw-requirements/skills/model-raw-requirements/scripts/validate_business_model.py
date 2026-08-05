#!/usr/bin/env python3
"""Validate a Markdown business-model bundle produced from raw requirements."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


FEATURE_PATTERNS = {
    "process": re.compile(r"```mermaid\s+(?:flowchart|graph)\b", re.IGNORECASE),
    "sequence": re.compile(r"```mermaid\s+sequenceDiagram\b", re.IGNORECASE),
    "state": re.compile(r"```mermaid\s+stateDiagram(?:-v2)?\b", re.IGNORECASE),
    "erd": re.compile(r"```mermaid\s+erDiagram\b", re.IGNORECASE),
    "rules": re.compile(r"\bBR-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b"),
}

RULE_ID = re.compile(r"\bBR-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b")
DECISION_ID = re.compile(r"\bDQ-\d{3}\b")
RULE_DEFINITION = re.compile(
    r"(?m)^\s*(?:#{1,6}\s+|\|\s*|[-*]\s+\*{0,2})"
    r"(BR-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3})\b"
)
DECISION_DEFINITION = re.compile(
    r"(?m)^\s*(?:#{1,6}\s+|\|\s*|[-*]\s+\*{0,2})(DQ-\d{3})\b"
)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+\.md)(?:#[^)]+)?\)")
TYPE_FIELD = re.compile(r"^type:\s*\S.*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Business-model Markdown file or directory")
    parser.add_argument(
        "--expect",
        default="process,sequence,state,erd,rules",
        help="Comma-separated required features: process,sequence,state,erd,rules",
    )
    return parser.parse_args()


def markdown_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix.lower() == ".md":
        return [root]
    if root.is_dir():
        return sorted(root.rglob("*.md"))
    return []


def frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    return text[4:end]


def resolve_link(root: Path, source: Path, target: str) -> Path | None:
    if re.match(r"^[a-z][a-z0-9+.-]*://", target, re.IGNORECASE):
        return None
    clean = target.split("#", 1)[0]
    if clean.startswith("/Users/") or clean.startswith("/home/") or clean.startswith("/tmp/"):
        return Path(clean)
    if clean.startswith("/"):
        return root / clean.lstrip("/")
    return source.parent / clean


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    files = markdown_files(root)
    model_root = root if root.is_dir() else root.parent
    errors: list[str] = []
    warnings: list[str] = []

    if not files:
        print(f"ERROR: no Markdown files found under {root}")
        return 1

    texts: dict[Path, str] = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        texts[path] = text
        if text.count("```") % 2:
            errors.append(f"{path.relative_to(model_root)}: unmatched fenced code block")

        if path.name not in {"index.md", "log.md"}:
            header = frontmatter(text)
            if header is None:
                errors.append(f"{path.relative_to(model_root)}: missing OKF YAML frontmatter")
            elif not TYPE_FIELD.search(header):
                errors.append(f"{path.relative_to(model_root)}: missing non-empty OKF type")

        for target in MD_LINK.findall(text):
            resolved = resolve_link(model_root, path, target)
            if resolved is not None and not resolved.exists():
                errors.append(
                    f"{path.relative_to(model_root)}: broken Markdown link {target}"
                )

    combined = "\n".join(texts.values())
    expected = [item.strip() for item in args.expect.split(",") if item.strip()]
    unknown = sorted(set(expected) - set(FEATURE_PATTERNS))
    if unknown:
        errors.append(f"unknown --expect feature(s): {', '.join(unknown)}")
    for feature in expected:
        pattern = FEATURE_PATTERNS.get(feature)
        if pattern and not pattern.search(combined):
            errors.append(f"missing required model feature: {feature}")

    mentioned_rule_ids = RULE_ID.findall(combined)
    mentioned_decision_ids = DECISION_ID.findall(combined)
    rule_ids = RULE_DEFINITION.findall(combined)
    decision_ids = DECISION_DEFINITION.findall(combined)
    for identifier, count in Counter(rule_ids).items():
        if count > 1:
            errors.append(f"duplicate business-rule ID: {identifier} ({count} occurrences)")
    for identifier, count in Counter(decision_ids).items():
        if count > 1:
            errors.append(f"duplicate decision ID: {identifier} ({count} occurrences)")

    if not mentioned_decision_ids:
        warnings.append("no DQ-NNN decision IDs found; verify that no ambiguity was suppressed")
    if not re.search(r"(source|来源|引用|traceab)", combined, re.IGNORECASE):
        warnings.append("no obvious source/traceability section found")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    print(
        f"SUMMARY: files={len(files)} rules={len(set(rule_ids or mentioned_rule_ids))} "
        f"decisions={len(set(decision_ids or mentioned_decision_ids))} "
        f"errors={len(errors)} warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
