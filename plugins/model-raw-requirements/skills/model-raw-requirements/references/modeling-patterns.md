# Business Modeling Patterns

## Contents

- Source arbitration
- Model contracts
- Cross-model consistency
- Common failure modes
- Default deliverable shape

## Source arbitration

Use this precedence only as a starting heuristic; preserve unresolved conflict when authority is unclear.

1. Explicit current business policy or authorized stakeholder decision.
2. Observed operational workflow, including exception handling.
3. Approved product requirement or acceptance criterion.
4. Architecture/design proposal.
5. Prototype behavior, implementation default, or illustrative number.

Treat `must`, named decision authority, and explicit exception rules as stronger than aspirational language. Treat recency as evidence only when versions are comparable. Never infer approval merely because a draft is more detailed.

Recommended certainty labels:

- `confirmed`: supported by authoritative or mutually consistent sources.
- `inferred`: needed for model coherence but not stated directly.
- `draft-default`: useful starting value or behavior, not approved business policy.
- `conflicting`: sources disagree in a way that affects behavior.
- `unresolved`: required decision has no adequate source.

## Model contracts

### Business process

Show the end-to-end business outcome, not a screen tour.

- Include start, outcome, decision branches, responsible actor, exception path, escalation, and recovery.
- Merge entry channels after their meaningful differences end.
- Keep optional automation as a side path when the core outcome can continue manually.
- Do not draw separate processes for channels that share the same downstream business flow.

### Sequence

Show who exchanges which business message and in what order.

- Include human decision makers, the system of record, external systems, and field/operational actors.
- Distinguish `sent`, `delivered`, `acknowledged`, `accepted`, `started`, and `completed` when they are separate facts.
- Show parallel notifications, timeouts, callbacks, retry/escalation, cancellation, and idempotency where relevant.
- Keep UI components out unless they own meaningful behavior.

### State machine

Create one state machine per aggregate that owns a lifecycle.

- Use durable fact names such as `PendingReview`, `Accepted`, or `Archived`.
- Label transitions with business events and important guards.
- Identify terminal states, cancellation semantics, backward transitions, and amendment behavior.
- Split parent event/order/case state from assignment, delivery, payment, approval, or external receipt states.
- Do not use a state as a substitute for a reason; keep closure/result reason separately.

### Entity relationship

Model durable business facts needed to execute and audit the process.

- Start from nouns in decisions, transitions, evidence, ownership, and outputs.
- Prefer structured entities for core facts over a catch-all JSON field.
- Preserve source observations, analyses, locations, evidence, assignments, attempts, reports, receipts, and state transitions when they change independently.
- Add cardinalities that support retries, reassignment, multi-party work, corrections, and history.
- Record identifiers, timestamps, actor references, status, and provenance where auditability matters.

### Business rules

Write one testable obligation or constraint per rule.

- Use stable IDs such as `BR-DSP-001`.
- Include rule status/certainty and source reference.
- Separate policy from configurable parameters.
- Express authority, required data, transition guards, timeout behavior, exception handling, security, audit, and retention rules.
- Avoid compound rules joined by several unrelated conditions.

### Decision backlog

Use stable IDs such as `DQ-001`.

For each item record:

- the exact decision required;
- conflicting or missing source positions;
- a recommended starting option, clearly labeled as a recommendation;
- affected process, state, data, rule, UI, integration, or acceptance criteria;
- owner and decision date when available.

## Cross-model consistency

Verify these mappings:

- Every material process decision has a rule or a decision item.
- Every sequence-changing business event is a valid state transition.
- Every state transition has an actor or system trigger and required stored data.
- Every durable message, assignment, result, evidence item, and transition maps to an entity.
- Every entity status belongs to the correct aggregate state machine.
- Every exception branch has a terminal, retry, reassignment, escalation, or manual fallback.
- Every external integration has independent delivery/receipt semantics.

## Common failure modes

- Copying source prose into diagrams without resolving contradictions.
- Treating architecture automation as approved business authority.
- Using one universal status for a case plus all of its tasks and channels.
- Equating algorithm confidence with a final business conclusion.
- Equating notification delivery with human acceptance or real-world completion.
- Losing original evidence or analysis when a later result arrives.
- Creating duplicate cases for follow-up observations of the same real-world incident.
- Burying thresholds, permissions, and future scope inside narrative instead of decision items.
- Modeling database tables before understanding the business lifecycle.

## Required OKF deliverable shape

Always create or update an OKF v0.1 bundle under `docs/okf/`, regardless of the project's existing documentation convention. Use this as a starting shape and add only concepts required by the project:

```text
docs/okf/
  index.md
  log.md
  project.md
  requirements/
    index.md
    business-process.md
    sequence-model.md
    state-machines.md
    business-rules.md
  data-models/
    index.md
    domain-model.md
  decisions/
    index.md
    open-decisions.md
  references/
    index.md
    source-materials.md
```

Keep model files focused and cross-linked. Follow `okf-project-docs` for frontmatter, indexes, log ordering, citations, link style, compatibility, and validation. Existing non-OKF documentation may be cited or summarized as source material but must not replace this bundle structure.
