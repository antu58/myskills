#!/usr/bin/env python3
"""Build a self-contained static viewer for an OKF Markdown bundle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
TYPE_RE = re.compile(r"^type:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def metadata(text: str, path: Path) -> dict[str, str]:
    frontmatter = ""
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            frontmatter = text[4:end]
            body = text[end + 5 :]

    title = TITLE_RE.search(frontmatter) or HEADING_RE.search(body)
    description = DESCRIPTION_RE.search(frontmatter)
    concept_type = TYPE_RE.search(frontmatter)
    return {
        "title": title.group(1).strip() if title else ("首页" if path.as_posix() == "index.md" else path.stem),
        "description": description.group(1).strip() if description else "",
        "type": concept_type.group(1).strip() if concept_type else ("Index" if path.name == "index.md" else "Log" if path.name == "log.md" else "Document"),
    }


def build(bundle_root: Path, output_name: str) -> Path:
    root = bundle_root.resolve()
    if not root.is_dir():
        raise ValueError(f"bundle root is not a directory: {root}")
    if Path(output_name).name != output_name:
        raise ValueError("--output must be a filename placed at the bundle root")

    files = []
    for path in sorted(root.rglob("*.md"), key=lambda item: (len(item.relative_to(root).parts), item.as_posix())):
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts):
            continue
        content = path.read_text(encoding="utf-8")
        files.append({"path": relative.as_posix(), "content": content, **metadata(content, relative)})

    skill_root = Path(__file__).resolve().parent.parent
    template = (skill_root / "assets" / "okf-viewer" / "template.html").read_text(encoding="utf-8")
    runtime = (skill_root / "assets" / "okf-viewer" / "mermaid.min.js").read_text(encoding="utf-8")
    if template.count("__OKF_DATA__") != 1 or template.count("/*__MERMAID_RUNTIME__*/") != 1:
        raise ValueError("viewer template placeholders are missing or duplicated")

    payload = json.dumps({"version": 1, "files": files}, ensure_ascii=True, separators=(",", ":"))
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = template.replace("__OKF_DATA__", payload).replace(
        "/*__MERMAID_RUNTIME__*/", runtime.replace("</script", "<\\/script")
    )
    output = root / output_name
    output.write_text(html, encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained OKF Markdown viewer.")
    parser.add_argument("bundle_root", type=Path)
    parser.add_argument("--output", default="viewer.html")
    args = parser.parse_args()
    output = build(args.bundle_root, args.output)
    print(f"BUILT: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
