# AGENT_AGENT0_OUTBOX.md
> Purpose: Single inbox/outbox for IDE extensions (0A/0B/0C).
> Rule: Extensions append entries here; Agent 1 reads and then updates AGENT_HANDOVER.md / AGENT_DECISIONS.md as needed.
> Default: No production file edits. This is advisory output.

---

## HOW TO USE (FOR EXTENSIONS)
1) Read:
   - `docs/INFO_AI_RULES.md`
   - `docs/INFO_IDE_EXTENSIONS_ROLE.md`
   - `docs/AGENT_HANDOVER.md`
   - plus any user-named file(s)
2) Append a new entry under your agent section (0A/0B/0C).
3) Do NOT edit other agents’ sections.
4) Do NOT edit production code unless explicitly asked.
5) If you did edit code (explicit request), also log in `docs/AGENT_HANDOVER.md` using the `[EXT_EDIT_LOG]` block.

---

## Agent 0A — Entries

### [ENTRY TEMPLATE]
- **Timestamp (local):**
- **Request / Task:**
- **Mode:** Planner | Reviewer | Implementer (explicit)
- **Context files read:** (list)
- **Proposed plan / critique:**
  1)
  2)
  3)
- **Files suggested to touch:** (paths)
- **No-go zones:** (paths / rules)
- **Risks / edge cases:**
  -
- **Verification checklist (commands/tests + expected result):**
  -
- **Rollback plan:**
  -
- **Handover note for Agent 1 (copy-paste):**
  -

---