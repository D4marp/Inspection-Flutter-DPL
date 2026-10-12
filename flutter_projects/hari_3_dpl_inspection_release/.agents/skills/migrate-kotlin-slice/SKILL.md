---
name: migrate-kotlin-slice
description: Migrate one reviewable Android Kotlin/XML vertical slice to this Flutter inspection app while preserving documented behavior and acceptance criteria. Use for Kotlin discovery, mapping, implementation, parity testing, or migration review; exclude unrelated feature development.
metadata:
  opencode/slash: "true"
  audience: "flutter-training"
---

# Migrate a Kotlin Slice

Work on one vertical slice at a time. Treat the PRD and observed legacy behavior as the contract; do not infer missing API fields or business rules.

## Required context

Read only the relevant inputs before editing:

- `docs/PRD_MIGRASI_KOTLIN.md`
- sanitized Kotlin/XML files supplied by the trainer for the selected slice
- the target Flutter screen, model, controller, and tests

Legacy source is intentionally not bundled in this project. If it has not been
supplied, stop before implementation and report the missing evidence. If a rule
is absent or contradictory, label it as an unknown and ask for a product
decision instead of choosing silently.

## Workflow

1. Summarize the legacy state, events, validation, navigation, and edge cases.
2. Link each behavior to an acceptance criterion and planned evidence.
3. Propose a small file-scoped plan. Keep native Flutter for core interaction; use WebView only when the PRD identifies it as a transition boundary.
4. Implement the smallest coherent patch. Preserve identifiers, terms, ordering, and failure semantics.
5. Add or update tests for the risky behavior, then run formatter, analyzer, and tests.
6. Report changed files, parity evidence, assumptions, residual risks, and the next slice.

## Guardrails

- Never place API keys, tokens, PII, or production payloads in source, prompts, fixtures, or logs.
- Do not rewrite unrelated layers or add a dependency without explaining why the slice needs it.
- Preserve the PRD WebView boundary: JavaScript may run for the approved training site, but do not add a bridge or broaden the HTTPS host allowlist merely to make a page load.
- Do not describe a build or test as successful unless its command actually passed.
- Keep the result understandable without relying on chat history.
