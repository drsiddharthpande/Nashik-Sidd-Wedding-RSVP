# AG_AI_OS_TEMPLATE

## Purpose
This is the **template repository** for all new AI OS projects. Clone or fork this repo to start any new project with the full AI OS scaffold pre-configured.

## AI OS Structure

```
docs/                     — All AI OS control + info files
  INFO_AI_RULES.md        — Workspace doctrine (read first)
  INFO_IDE_EXTENSIONS_ROLE.md — IDE extension contract
  INFO_FILE_NAMES.md      — Naming conventions
  AGENT_HANDOVER.md       — Mission control (phase gates)
  AGENT_DECISIONS.md      — Decision log
  AGENT_STATUS.json       — Machine-readable phase gate
  AGENT_API_TRACE.jsonl   — OpenAI call trace (append-only)
  AGENT_AGENT0_OUTBOX.md  — IDE extension outbox
  CHANGE_LOG.md           — Human-readable change history
  reviews/                — Saved OpenAI review outputs

ops/                      — Automation + review scripts
src/                      — Application source code
data/
  db/migrations/          — Schema migration files
  lib/                    — Quick-access JSON libraries
  libdb/                  — Large queryable reference DBs
  cache/                  — Regeneratable derived artifacts
logs/                     — Log files
temp/                     — Throwaway scripts (TEMP_*)

.agents/workflows/        — AI workflow definitions
  boot.md                 — /boot workflow
  review.md               — /review workflow
  ship.md                 — /ship workflow
```

## Quick Start

1. Clone this repo into your new project folder.
2. Open the project in your IDE.
3. Tell the AI agent: **Run /boot**
4. The agent will read the doctrine files and initialize PHASE_1.

## Key Workflows

| Command   | Purpose                                          |
|-----------|--------------------------------------------------|
| `/boot`   | Initialize repo + read all doctrine docs         |
| `/review` | Run GPT architecture/security review             |
| `/ship`   | End-of-task closure + cleanup + final commit     |

---

_Managed by the AI OS architecture. See `docs/INFO_AI_RULES.md` for full doctrine._
