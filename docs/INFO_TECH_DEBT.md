# INFO_TECH_DEBT.md — Technical Debt Register

## Purpose
Tracks known technical debt, shortcuts taken, and refactoring targets. Reviewed by Agent 1 at the start of each major phase.

> **Fill this in** as tech debt is identified. Delete this instruction block when done.

---

## Active Debt Items

| ID | Description | Area | Severity | Added On | Target Phase |
|----|-------------|------|----------|----------|--------------|
| TD-001 | _[e.g. Hardcoded config values in src/app.py]_ | _[Backend]_ | `HIGH` \| `MED` \| `LOW` | _[YYYY-MM-DD]_ | _[PHASE_N]_ |

---

## Resolved Debt

| ID | Description | Resolved On | Resolution |
|----|-------------|-------------|------------|
| — | _[No resolved items yet]_ | — | — |

---

## Debt Guidelines

- **HIGH**: Blocks production correctness or security — resolve within current phase.
- **MED**: Degrades maintainability — schedule within next 2 phases.
- **LOW**: Cosmetic or non-urgent — address during `/ship` cleanup.

---

_Last updated: [YYYY-MM-DD]_
