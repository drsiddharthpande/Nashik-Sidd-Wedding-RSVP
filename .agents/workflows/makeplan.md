---
description: Architect-only phased planning (NO implementation, NO code edits)
---

# /makeplan — Phased Planning (Agent 1 Only)

This workflow is for **Agent 1 only**. No code is written, no files are edited outside of `docs/`. The output is a fully gated phase plan in `AGENT_HANDOVER.md` and an updated `AGENT_STATUS.json`.

> [!IMPORTANT]
> Agent 2 must NOT execute until Agent 1 has set a phase to ACTIVE in `AGENT_STATUS.json`.

---

## Steps

1. **Read all doctrine files** in order (mandatory before planning):
   - `docs/INFO_AI_RULES.md`
   - `docs/INFO_IDE_EXTENSIONS_ROLE.md`
   - `docs/AGENT_HANDOVER.md`
   - `docs/AGENT_STATUS.json`
   - `docs/AGENT_AGENT0_OUTBOX.md`
   - `docs/CHANGE_LOG.md`

2. **Read the project context** (if they exist):
   - `docs/INFO_GOAL.md`
   - `docs/INFO_VISION.md`
   - `docs/INFO_STATUS.md`
   - `docs/INFO_TECH_DEBT.md`

3. **Understand the user's request** — ask clarifying questions if needed before planning.

4. **Design phases** — break the work into numbered phases:
   - Each phase must have a clear goal, executor, and definition of done.
   - Only ONE phase may be ACTIVE at a time.
   - Future phases go behind `<!-- LOCKED_TASKS_BEGIN -->` markers.

5. **Write / update `docs/AGENT_HANDOVER.md`**:
   - Use the standard phase header format:
     ```
     ## PHASE_<N> — <NAME>  [STATUS: ACTIVE|COMPLETED|BLOCKED]  [EXECUTOR: AGENT_1|AGENT_2]
     ```
   - Set the first phase to `ACTIVE`.
   - Lock all future phases.

6. **Update `docs/AGENT_STATUS.json`**:
   - Set `active_phase` to the first phase ID.
   - Set `agent2_lock.allowed_phase_id` to the same phase ID.

7. **Update `docs/AGENT_DECISIONS.md`**:
   - Add a decision record for any significant architectural choices made during planning.

8. **Update `docs/CHANGE_LOG.md`**:
   - Add a `/makeplan` entry with date and summary of what was planned.

9. **Report to user**:
   - List all phases planned.
   - State which phase is ACTIVE and what Agent 2 should do next.
   - Do NOT begin implementation.
