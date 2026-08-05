#!/usr/bin/env python3
"""Validate the basic OKF v0.1 structure of a knowledge bundle."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on host environment
    yaml = None


RESERVED = {"index.md", "log.md"}
DATE_HEADING_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$")


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed with ---")
    raw = text[4:end]
    if yaml is None:
        data = parse_minimal_yaml(raw)
    else:
        loaded = yaml.safe_load(raw) if raw.strip() else {}
        if not isinstance(loaded, dict):
            raise ValueError("frontmatter must parse to a mapping")
        data = loaded
    return data, text[end + 5 :]


def parse_minimal_yaml(raw: str) -> dict:
    data: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError("frontmatter contains unsupported YAML syntax; install PyYAML for full parsing")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def validate_bundle(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"{root}: bundle root does not exist"], warnings
    if not root.is_dir():
        return [f"{root}: bundle root is not a directory"], warnings

    markdown_files = sorted(p for p in root.rglob("*.md") if p.is_file())
    if not markdown_files:
        warnings.append(f"{root}: no Markdown files found")

    for path in markdown_files:
        rel = path.relative_to(root)
        if path.name == "index.md":
            validate_index(path, rel, root, errors, warnings)
        elif path.name == "log.md":
            validate_log(path, rel, errors, warnings)
        else:
            validate_concept(path, rel, errors, warnings)

    if not (root / "index.md").exists():
        warnings.append("root index.md is missing; OKF allows this, but an index improves navigation")

    return errors, warnings


def validate_concept(path: Path, rel: Path, errors: list[str], warnings: list[str]) -> None:
    try:
        frontmatter, body = parse_frontmatter(path)
    except Exception as exc:
        errors.append(f"{rel}: {exc}")
        return

    concept_type = frontmatter.get("type")
    if not isinstance(concept_type, str) or not concept_type.strip():
        errors.append(f"{rel}: frontmatter must include a non-empty type")

    for field in ("title", "description", "tags", "timestamp"):
        if field not in frontmatter:
            warnings.append(f"{rel}: recommended frontmatter field missing: {field}")

    if "# Citations" not in body and "# 引用" not in body:
        warnings.append(f"{rel}: consider adding # Citations or # 引用 when claims depend on sources")


def validate_index(path: Path, rel: Path, root: Path, errors: list[str], warnings: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    is_root_index = path == root / "index.md"
    if text.startswith("---\n"):
        if not is_root_index:
            errors.append(f"{rel}: only the bundle-root index.md may include frontmatter")
            return
        try:
            frontmatter, _ = parse_frontmatter(path)
        except Exception as exc:
            errors.append(f"{rel}: invalid root index frontmatter: {exc}")
            return
        extra_keys = sorted(k for k in frontmatter if k != "okf_version")
        if extra_keys:
            warnings.append(f"{rel}: root index frontmatter should only declare okf_version, found: {', '.join(extra_keys)}")
    if not re.search(r"^\s*[*-]\s+\[.+?\]\(.+?\)", text, re.MULTILINE):
        warnings.append(f"{rel}: index should contain Markdown list links to child concepts or subdirectories")


def validate_log(path: Path, rel: Path, errors: list[str], warnings: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        errors.append(f"{rel}: log.md must not include frontmatter")
        return
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    invalid = [line for line in headings if not DATE_HEADING_RE.match(line)]
    if invalid:
        errors.append(f"{rel}: log date headings must use YYYY-MM-DD")
    if not headings:
        warnings.append(f"{rel}: log.md should contain date headings like ## 2026-06-23")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a basic OKF v0.1 knowledge bundle.")
    parser.add_argument("bundle_root", type=Path)
    args = parser.parse_args()

    errors, warnings = validate_bundle(args.bundle_root)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
