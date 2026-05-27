---
description: Initialize standard repo folders + required docs (INFO_AI_RULES, AGENT files, CHANGE_LOG) and open the doctrine files in the correct order.
---

# /boot — Repository Initialization

This workflow runs when a new repo is blank or missing standard AI OS scaffolding.

// turbo-all

## Steps

1. **Read GLOBAL AI OS RULES** from agent memory (already loaded).

2. **Check for existing standard docs** — list `docs/` to see what already exists.

3. **Create missing standard folders** if they don't exist:
   - `docs/`, `docs/reviews/`, `docs/legacy/`
   - `ops/`
   - `src/`
   - `data/db/migrations/`, `data/lib/`, `data/libdb/`, `data/cache/`
   - `logs/`
   - `temp/`
   - `.agents/workflows/`

4. **Create or verify all required docs** (create only if missing):
   - `docs/INFO_AI_RULES.md` — workspace doctrine
   - `docs/INFO_IDE_EXTENSIONS_ROLE.md` — IDE extension contract
   - `docs/INFO_FILE_NAMES.md` — naming conventions
   - `docs/AGENT_HANDOVER.md` — mission control with PHASE_1 ACTIVE
   - `docs/AGENT_DECISIONS.md` — decision log
   - `docs/AGENT_STATUS.json` — machine gate, PHASE_1 ACTIVE
   - `docs/AGENT_API_TRACE.jsonl` — empty append-only trace
   - `docs/AGENT_AGENT0_OUTBOX.md` — extension outbox
   - `docs/CHANGE_LOG.md` — with initial /boot entry

5. **Create or verify workflow files**:
   - `.agents/workflows/boot.md` (this file)
   - `.agents/workflows/review.md`
   - `.agents/workflows/ship.md`

6. **Update README.md** with repo purpose and link to AI OS structure.

7. **Add `.gitkeep`** to all empty folders so git tracks them.

8. **Make initial git commit**:
   ```
   git add -A
   git commit -m "chore: /boot — AI OS scaffold (PHASE_1)"
   ```

9. **Open doctrine files in order** (read, do not edit):
   - `docs/INFO_AI_RULES.md`
   - `docs/INFO_IDE_EXTENSIONS_ROLE.md`
   - `docs/AGENT_HANDOVER.md`
   - `docs/AGENT_STATUS.json`
   - `docs/AGENT_AGENT0_OUTBOX.md`
   - `docs/CHANGE_LOG.md`

10. **Report to user**: State which files were created, what PHASE_1 goal is, and what the next action is.
