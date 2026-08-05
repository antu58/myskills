---
name: model-raw-requirements
description: Convert fragmented, informal, or conflicting project-start requirements into a reviewable OKF v0.1 business-model bundle. Use when Codex must synthesize DOCX/PDF/spreadsheets, wiki pages, tickets, meeting notes, chats, emails, screenshots, legacy specifications, or stakeholder statements into business scope, actors, process flows, sequence diagrams, state machines, entity relationships, atomic business rules, source traceability, and an explicit decision backlog before product or engineering design begins. Always use the okf-project-docs convention regardless of the project's existing documentation format.
---

# Model Raw Requirements

Turn raw requirement material into a coherent business model without silently promoting guesses, architecture proposals, or prototype defaults into approved business requirements.

## Workflow

1. Inspect the project before writing.
   - Read applicable `AGENTS.md`, existing requirements, architecture notes, code, and documentation as sources.
   - Invoke `okf-project-docs` and follow its current instructions.
   - If `okf-project-docs` is unavailable, report the blocker instead of inventing a substitute convention.
   - Always create or update the OKF bundle at `docs/okf/`, regardless of the project's existing documentation format. Treat non-OKF documentation as input material, not as the output convention.
   - Preserve compatible existing OKF concepts, unknown frontmatter fields, and links when updating an existing bundle.

2. Acquire and normalize the source material.
   - Use the relevant document, PDF, spreadsheet, browser, connector, image, or code-reading skill for each source type.
   - Extract tables, embedded workbooks, diagrams, comments, and attachments when they carry requirements.
   - Follow explicit source limits. If the user says local files are authoritative, do not replace them with web research.
   - Record source filename or URL, version/date when known, and enough section context to trace conclusions.

3. Build a source ledger before modeling.
   - Classify each meaningful statement as `confirmed`, `inferred`, `draft-default`, `conflicting`, or `unresolved`.
   - Prefer operational descriptions for real business behavior and architecture documents for technical constraints.
   - Prefer explicit actor authority over implied automation.
   - When sources disagree, preserve the disagreement as a decision item; do not hide it with a blended sentence.
   - Continue modeling with explicit uncertainty instead of blocking on every ambiguity. Ask only when a missing source, authority, or user choice would materially change the permitted work.

4. Establish scope and vocabulary.
   - State the project goal, in-scope outcome, non-goals, actors, authority boundaries, external systems, and glossary.
   - Separate the minimum viable business loop from future automation and platform extensions.

5. Model in dependency order.
   - Produce all five core models unless the user explicitly limits the deliverable.
   - Create the business process first, including exceptions and recovery paths.
   - Create the interaction sequence from the process and actor responsibilities.
   - Create one state machine per lifecycle-owning aggregate; do not combine event, task, delivery, payment, approval, or external receipt states.
   - Derive the entity relationship model from durable business facts needed by those flows and states.
   - Express constraints as atomic, testable business rules with stable IDs.
   - Capture every unresolved threshold, role, channel, field requirement, or scope boundary in a decision backlog.

6. Reconcile instead of transcribing.
   - Separate observation from business fact, recommendation from authority, task from notification attempt, and external acknowledgement from real-world completion.
   - Treat timeouts, retries, token lifetimes, file-size limits, and similar numbers as draft defaults unless the business source approves them.
   - Preserve original and revised analysis, locations, evidence, and state transitions when auditability matters.
   - Make degraded paths explicit so optional automation or failing integrations cannot silently block the core business outcome.

7. Write a navigable OKF model bundle.
   - Produce `docs/okf/index.md`, `log.md`, a project overview, and separate process, sequence, state, entity, rule, decision, and source-reference concepts.
   - Give every non-reserved concept file valid YAML frontmatter with a non-empty `type`; keep `index.md` and `log.md` within OKF reserved-file rules.
   - Use Mermaid for static flow, sequence, state, and ER diagrams.
   - Use `BR-<AREA>-NNN` for rule IDs and `DQ-NNN` for open decisions unless the project already defines identifiers.
   - Use bundle-root absolute links, navigational indexes, a newest-first log entry, and `# 引用`/`# Citations` sections for sourced claims.
   - Cross-link artifacts so a reviewer can move from a process branch to its state, data, rule, and unresolved decision.

8. Validate before delivery.
   - Run `scripts/validate_business_model.py docs/okf` from this skill.
   - Run the official `okf-project-docs` bundle validator after the business-model validator.
   - Fix duplicate identifiers, missing model types, unmatched Mermaid fences, and broken internal Markdown links.
   - Review the quality gate below; do not claim a decision is approved when it is only recommended.

## Quality Gate

- The main business outcome has a start, a terminal result, branch owners, exception paths, and manual fallback.
- Sequence messages distinguish requests, acknowledgements, business decisions, and asynchronous callbacks.
- State names describe durable facts rather than button clicks or temporary UI labels.
- Each aggregate has its own lifecycle; channel failures do not overwrite the parent business state.
- Entities represent business nouns and auditable facts, not screens or arbitrary JSON bags.
- Rules are atomic, testable, sourced, and marked by certainty.
- Conflicts, authority questions, numeric defaults, and future-scope items are visible in the decision backlog.
- Every material conclusion is traceable to a source or explicitly labeled as a modeling inference.
- The output is an OKF v0.1 bundle and passes both business-model and OKF validators with no errors or warnings.

## References

Read [references/modeling-patterns.md](references/modeling-patterns.md) when designing the five models, resolving common source conflicts, or reviewing model quality.
