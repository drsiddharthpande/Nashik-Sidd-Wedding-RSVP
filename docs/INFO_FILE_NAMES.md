# AI-OS — File Naming Conventions & Standard Docs

## Documentation Files (`docs/`)

### Human-Facing (`INFO_*`)
| File | Purpose |
|------|---------|
| `INFO_AI_RULES.md` | Workspace doctrine: API rules, naming law, agent behavior |
| `INFO_GOAL.md` | Project goals and therapeutic objectives |
| `INFO_STATUS.md` | Current development status |
| `INFO_TECH_DEBT.md` | Technical debt and refactoring targets |
| `INFO_HOW_TO_RUN.md` | Launch instructions |
| `INFO_VISION.md` | Product vision |
| `INFO_IDE_EXTENSIONS_ROLE.md` | Role contract for IDE extensions (Agent 0A/0B/0C): identification, default behavior, and logging rules |

### Agent-Operational (`AGENT_*`)
| File | Purpose |
|------|---------|
| `AGENT_HANDOVER.md` | Inter-agent baton: missions, phases, gating |
| `AGENT_DECISIONS.md` | Decision records (ADR-lite) |
| `AGENT_STATUS.json` | Machine-readable phase state |
| `AGENT_API_TRACE.jsonl` | OpenAI call trace (append-only) |
| `AGENT_AGENT0_OUTBOX.md` | External IDE extension outbox: plans/critiques from Agent 0A/0B/0C for Agent 1 intake (append-only by default) |

### Others
| File | Purpose |
|------|---------|
| `CHANGE_LOG.md` | Human timeline of major changes |
| `reviews/REVIEW_*.md` | External review outputs |
| `legacy/` | Quarantined deprecated files |

---

## Data Files (`data/`)

| Prefix | Location | Purpose |
|--------|----------|---------|
| `DB_*` | `data/db/` | Application databases (e.g., `DB_SESSION.json`) |
| `MIG_*` | `data/db/migrations/` | Schema migrations |
| `LIB_*` | `data/lib/` | Quick-access JSON libraries (e.g., `LIB_PROJECT_INDEX.json`) |
| `LIB_DB_*` | `data/libdb/` | Large queryable databases |
| `CACHE_*` | `data/cache/` | Regeneratable derived artifacts |

---

## Temporary Files

| Prefix | Location | Purpose |
|--------|----------|---------|
| `TEMP_*` | `temp/` | Disposable scripts/utilities |
| `DEBUG_*` | `temp/` or `logs/` | Debug dumps (deletable) |

---

## External API Calls

| Prefix | Usage |
|--------|-------|
| `REVIEW_*` | Call tags for OpenAI reviews, saved to `docs/reviews/` |