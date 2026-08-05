---
name: okf-project-docs
description: Create, restructure, or update project documentation as an Open Knowledge Format (OKF) bundle with a generated static viewer, writing documentation in Chinese by default unless the user explicitly requests another language. Use when Codex needs to produce backend architecture docs, service/API/data/event/runbook/ADR documentation, knowledge-base files, or project docs that should be human-readable, agent-readable, Git-diffable, cross-linked Markdown with YAML frontmatter following OKF v0.1, especially when Mermaid flowcharts or sequence diagrams need drag-and-zoom browsing.
---

# OKF Project Docs

## Overview

Create project documentation as an OKF knowledge bundle: a directory tree of Markdown concept files with YAML frontmatter, indexes for progressive disclosure, links that make relationships explicit, and a generated `viewer.html` for visual browsing.

Follow OKF v0.1 unless the user provides a newer version or a project-specific convention. Read `references/okf-v0-1.md` when you need exact rules, templates, or backend architecture type suggestions.

## Language Priority

Write generated documentation in Chinese by default. 默认优先使用中文撰写项目文档。Use another language only when the user explicitly requests it or when an existing project documentation set clearly uses that language and changing it would be disruptive. Prefer concise Chinese filenames for newly created non-reserved concept documents, such as `用户服务.md`, `支付回调.md`, and `故障恢复.md`. Keep reserved structural or generated filenames such as `index.md`, `log.md`, and `viewer.html` unchanged. Preserve existing filenames, and keep code identifiers, route names, config keys, protocol names, and established product names in their original form when they appear in filenames or content.

When adapting templates or examples from `references/okf-v0-1.md`, translate visible prose, section headings, descriptions, indexes, and log entries to Chinese. OKF `type` values may stay in concise English when that keeps machine-readable taxonomy stable.

## Workflow

1. Pick or create a bundle root, commonly `docs/okf/`, `knowledge/`, or the user-specified docs directory.
2. Identify concepts from the project: project overview, services, APIs, endpoints, databases, tables, events, queues, integrations, deployment, observability, security, runbooks, metrics, and decisions.
3. Create one concept per non-reserved `.md` file. Do not put many unrelated concepts into one large document.
4. Give every concept file YAML frontmatter with a non-empty `type`. Prefer also adding `title`, `description`, `tags`, and `timestamp`.
5. Use `index.md` files for directory navigation. Include short descriptions and links to child concepts.
6. Use `log.md` files only for chronological updates. Keep newest dates first.
7. Cross-link related concepts with Markdown links. Prefer bundle-root absolute links like `/services/user-service.md` when the bundle will be consumed as a standalone OKF directory.
8. Add a citations section when claims depend on source files, external docs, tickets, diagrams, or operational evidence. In Chinese docs, prefer `# 引用`; use `# Citations` only when writing English docs.
9. Write in Chinese by default unless the user explicitly requests another language. Name new non-reserved concept files in concise Chinese by default. Preserve reserved filenames, existing names, and code-derived filenames when renaming would reduce traceability or break links.
10. Run `scripts/validate_okf_bundle.py <bundle-root>` before finishing when files were created or changed.
11. Run `scripts/build_okf_viewer.py <bundle-root>` after Markdown changes so the bundle-root `viewer.html` embeds the current documents.
12. Open `viewer.html` in a browser for a smoke check when the bundle contains Mermaid diagrams or the viewer implementation changed.

## Static Viewer

- Treat `viewer.html` as a generated bundle artifact. Do not hand-edit it.
- Generate it from `assets/okf-viewer/template.html` with `scripts/build_okf_viewer.py`; the builder embeds the bundle's Markdown and Mermaid runtime into one portable HTML file.
- Build the navigation by recursively scanning Markdown files under the bundle root. Preserve each file's real bundle-relative path and original filename in the generated viewer; do not replace navigation labels with frontmatter titles.
- Keep it at the bundle root so the user can open it directly without starting a server or granting directory access.
- Preserve Mermaid source in fenced `mermaid` blocks. The viewer renders each diagram in a pan-and-zoom canvas with wheel zoom, pointer drag, fit/reset, and expanded view.
- Rebuild the viewer whenever any bundle Markdown changes. Do not include `viewer.html` in concept indexes or citations because it is a derived navigation artifact.

## Required OKF Rules

- A knowledge bundle is a directory tree of Markdown files.
- Reserved files are `index.md` and `log.md`; all other `.md` files are concept documents.
- Every concept document must start with parseable YAML frontmatter delimited by `---`.
- Every concept frontmatter block must contain a non-empty `type`.
- `index.md` normally has no frontmatter. The root `index.md` may include frontmatter only to declare `okf_version: "0.1"`.
- `log.md` date headings must use `YYYY-MM-DD`.
- Consumers must tolerate unknown `type` values, unknown extra frontmatter keys, missing optional fields, missing indexes, and broken links.

## Recommended Bundle Shape

Use only directories that match the project:

```text
docs/okf/
  index.md
  log.md
  project.md
  services/
  apis/
  data-models/
  tables/
  events/
  integrations/
  deployment/
  observability/
  security/
  runbooks/
  decisions/
  references/
```

## Concept Frontmatter

Use this baseline:

```markdown
---
type: Service
title: User Service
description: Owns user identity, profile, and account lifecycle workflows.
tags: [backend, identity]
timestamp: 2026-06-23T00:00:00+08:00
---
```

Add optional producer-defined fields when helpful, such as `owner`, `status`, `criticality`, `resource`, `source`, `version`, `system`, or `service`. Preserve unknown fields when editing existing OKF documents.

## Backend Documentation Conventions

- Use `Project` for the root business/system overview.
- Use `Service` for deployable services and modules with independent ownership.
- Use `API` for API groups and `API Endpoint` for individual important endpoints.
- Use `Database`, `Table`, `Data Model`, or `Message Topic` for persistent and streaming data assets.
- Use `Event` for domain events and async message payloads.
- Use `Integration` for external systems, vendors, and cross-system contracts.
- Use `Runbook` for operational procedures.
- Use `Metric` for business, product, and operational metric definitions.
- Use `Architecture Decision` for ADR-style decisions.
- Use `Security Control` for auth, permissions, secrets, privacy, and compliance controls.

## Useful Sections

Prefer structured Markdown sections over long prose. Choose sections that fit the concept. Use Chinese headings by default; English heading names below are conceptual labels, not required visible text:

- Services: `# 职责`, `# 依赖`, `# API`, `# 数据`, `# 运维`, `# 引用`.
- APIs: `# 契约`, `# 鉴权`, `# 请求`, `# 响应`, `# 错误`, `# 示例`, `# 引用`.
- Tables and models: `# 结构`, `# 关系`, `# 生产者`, `# 消费者`, `# 示例`, `# 引用`.
- Events: `# 载荷`, `# 生产者`, `# 消费者`, `# 顺序`, `# 重试与死信`, `# 引用`.
- Runbooks: `# 触发条件`, `# 影响`, `# 检查`, `# 步骤`, `# 回滚`, `# 升级`, `# 引用`.
- Decisions: `# 背景`, `# 决策`, `# 影响`, `# 备选方案`, `# 引用`.

## Validation

After creating or editing an OKF bundle, run:

```bash
python3 /path/to/okf-project-docs/scripts/validate_okf_bundle.py <bundle-root>
python3 /path/to/okf-project-docs/scripts/build_okf_viewer.py <bundle-root>
```

Treat validation errors as blockers. Treat warnings as prompts to improve navigability or metadata quality.
