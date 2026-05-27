---
description: Enforce change log + cleanup discipline at end of a major task. Execute Phase 4 (Cleanup Notes) and make a final commit.
---

# /ship — End-of-Task Closure

This workflow enforces proper documentation and cleanup discipline at the end of every major task.

## Steps

1. **Verify all phases are COMPLETED** in `docs/AGENT_STATUS.json`. If any phase is ACTIVE, stop and resolve it first.

2. **Run Phase 4 — Cleanup Notes**:
   - This is the ONLY time Phase 4 is executable (per GLOBAL AI OS RULES §10).
   - Tasks: remove temp files, remove TEMP_ scripts, archive DEBUG_ logs, update legacy/ for deprecated files.

3. **Update `docs/CHANGE_LOG.md`**:
   - Add a `[/ship]` entry summarizing all phases completed and any API response_ids used.

4. **Update `docs/AGENT_HANDOVER.md`**:
   - Mark PHASE_4 as COMPLETED.
   - Add a `## SHIP SUMMARY` section at the top with date, phases shipped, and who signed off.

5. **Update `docs/AGENT_STATUS.json`**:
   - Set `active_phase` to `null` or next project's PHASE_1.
   - Set all shipped phases to `COMPLETED`.

6. **Final git commit**:
   ```
   git add -A
   git commit -m "chore: /ship — <task name> complete (all phases done)"
   ```

7. **Report to user**: Confirm all phases are done, list files cleaned up, and confirm git commit hash.
