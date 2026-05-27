# CHANGE_LOG.md

## Purpose
Human-readable record of all major changes. Reference OpenAI response_ids for traced API calls.

---

## Entry Format
```
## [YYYY-MM-DD] — <Short description> (commit: <hash>)

- **Phase**: PHASE_N
- **Executor**: Agent 1 | Agent 2
- **Changes**:
  - Created/Modified/Deleted: `path/to/file`
- **API Calls**: `REVIEW_...` → response_id (or "None")
```

## [2026-05-27] — Set up RSVP form in index.html with Formspree URL (commit: 9414884)

- **Phase**: PHASE_2
- **Executor**: Antigravity
- **Changes**:
  - Created: `index.html` (renamed from `Index.html` to fix case-sensitivity lookup on Pages)
- **API Calls**: None

---

_Add entries above the line as changes are made._

