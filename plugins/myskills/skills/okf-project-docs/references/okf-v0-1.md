# OKF v0.1 Project Documentation Reference

Use this reference when creating or updating project documentation as an Open Knowledge Format bundle.

## Minimum Conformance

A bundle is conformant when:

1. Every non-reserved `.md` file contains a parseable YAML frontmatter block.
2. Every concept frontmatter block contains a non-empty `type`.
3. Reserved files follow their expected structure:
   - `index.md` is a directory listing.
   - `log.md` is a chronological update history.

Reserved filenames:

| Filename | Purpose |
| --- | --- |
| `index.md` | Directory listing for progressive disclosure |
| `log.md` | Chronological update history |

All other Markdown files are concept documents.

## Frontmatter Fields

Required:

| Field | Meaning |
| --- | --- |
| `type` | Short descriptive concept kind, such as `Service`, `API Endpoint`, `Table`, `Runbook`, or `Architecture Decision` |

Recommended:

| Field | Meaning |
| --- | --- |
| `title` | Human-readable display name |
| `description` | One-sentence summary for indexes, search snippets, and previews |
| `resource` | Canonical URI for the underlying asset when one exists |
| `tags` | YAML list of short categorization strings |
| `timestamp` | ISO 8601 last meaningful change time |

Allowed extensions:

| Field | Use |
| --- | --- |
| `owner` | Team or person responsible for the concept |
| `status` | `draft`, `active`, `deprecated`, or project-specific state |
| `criticality` | Operational importance such as `low`, `medium`, `high`, `critical` |
| `source` | Source path, URL, ticket, or discovery note |
| `service` | Owning service when documenting a nested asset |
| `system` | Owning system or bounded context |
| `version` | API, schema, or document version |

Consumers should preserve unknown fields and tolerate unknown `type` values.

## Bundle Layout For Backend Projects

Start with this shape and remove unused directories:

```text
docs/okf/
  index.md
  log.md
  project.md
  services/
    index.md
  apis/
    index.md
  data-models/
    index.md
  tables/
    index.md
  events/
    index.md
  integrations/
    index.md
  deployment/
    index.md
  observability/
    index.md
  security/
    index.md
  runbooks/
    index.md
  decisions/
    index.md
  references/
    index.md
```

## Root Index Template

````markdown
---
okf_version: "0.1"
---

# Project Knowledge Bundle

* [Project Overview](project.md) - System purpose, boundaries, and high-level architecture.
* [Services](services/) - Deployable services and owned modules.
* [APIs](apis/) - API groups, endpoints, auth, and contracts.
* [Data Models](data-models/) - Core domain models and schemas.
* [Tables](tables/) - Database tables and storage assets.
* [Events](events/) - Async events, topics, queues, and payloads.
* [Integrations](integrations/) - External systems and cross-system contracts.
* [Deployment](deployment/) - Runtime topology, environments, and release process.
* [Observability](observability/) - Metrics, dashboards, logging, tracing, and alerts.
* [Security](security/) - Auth, permissions, secrets, privacy, and compliance.
* [Runbooks](runbooks/) - Operational procedures.
* [Decisions](decisions/) - Architecture decisions and tradeoffs.
````

The root `index.md` is the only index file that may contain frontmatter, and only when declaring the OKF version.

## Directory Index Template

````markdown
# Services

* [User Service](user-service.md) - Owns user identity, profile, and account lifecycle workflows.
* [Billing Service](billing-service.md) - Owns subscription billing and payment reconciliation.
````

Use relative links in index files for local navigation.

## Log Template

```markdown
# Directory Update Log

## 2026-06-23
* **Creation**: Created the initial OKF bundle.
* **Update**: Added [User Service](/services/user-service.md).
```

Use ISO date headings in newest-first order.

## Concept Templates

### Service

```markdown
---
type: Service
title: User Service
description: Owns user identity, profile, and account lifecycle workflows.
tags: [backend, identity]
timestamp: 2026-06-23T00:00:00+08:00
---

# Responsibilities

-

# Dependencies

-

# APIs

-

# Data

-

# Operations

-

# Citations

[1] [Source](../path/to/source)
```

### API Endpoint

````markdown
---
type: API Endpoint
title: Create User
description: Creates a user account and starts the activation workflow.
tags: [api, users]
timestamp: 2026-06-23T00:00:00+08:00
---

# Contract

`POST /users`

# Authentication

-

# Request

```json
{}
```

# Response

```json
{}
```

# Errors

-

# Citations

[1] [OpenAPI source](../openapi.yaml)
````

### Table

```markdown
---
type: Table
title: Users
description: Stores user account identity and lifecycle status.
tags: [database, users]
timestamp: 2026-06-23T00:00:00+08:00
---

# Schema

| Column | Type | Description |
| --- | --- | --- |
| `id` | string | Unique user identifier. |

# Relationships

-

# Producers

-

# Consumers

-

# Citations

[1] [Migration source](../migrations/0001_users.sql)
```

### Event

````markdown
---
type: Event
title: UserCreated
description: Published after a user account is persisted.
tags: [event, users]
timestamp: 2026-06-23T00:00:00+08:00
---

# Payload

```json
{}
```

# Producers

-

# Consumers

-

# Ordering

-

# Retry And Dead Letter

-

# Citations

[1] [Event schema source](../schemas/user-created.json)
````

### Runbook

```markdown
---
type: Runbook
title: User Login Failure Spike
description: Steps to triage a sudden spike in login failures.
tags: [oncall, identity]
timestamp: 2026-06-23T00:00:00+08:00
---

# Trigger

-

# Impact

-

# Checks

-

# Steps

1.

# Rollback

-

# Escalation

-

# Citations

[1] [Alert source](../alerts/login-failures.yaml)
```

### Architecture Decision

```markdown
---
type: Architecture Decision
title: Use Object Storage For Client Uploads
description: Records the decision to store client-uploaded files in object storage.
tags: [architecture, storage]
timestamp: 2026-06-23T00:00:00+08:00
---

# Context

-

# Decision

-

# Consequences

-

# Alternatives

-

# Citations

[1] [Related design doc](/references/client-file-storage.md)
```

## Link Guidance

- Prefer bundle-root links (`/services/user-service.md`) inside concept bodies when linking concepts.
- Use relative links in `index.md` because indexes are directory-local navigation.
- Keep prose around links explicit: "depends on", "publishes", "consumes", "stores in", or "owned by".
- Broken links are allowed by OKF, but warn the user when important targets are missing.

## Writing Guidance

- Make each concept independently useful.
- Prefer tables, lists, fenced code blocks, and concise sections.
- Avoid unsupported claims. Add `# Citations` for code, docs, tickets, diagrams, and operational evidence.
- Preserve the user's language and project terminology.
- Keep filenames stable and lowercase hyphenated when creating new files.
