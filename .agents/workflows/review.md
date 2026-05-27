---
description: Run a GPT review using REVIEW_ call_tag discipline + Star Topology; save output to docs/reviews and append response_id trace to AGENT_API_TRACE.jsonl.
---

# /review — Run an External AI Review

> **Before starting:** Read `DOCS/INFO_AI_RULES.md` for full API rules.
> Key sections: **§1** (GPT-5.4 config), **§2a** (GPT-5.4 pricing), **§3** (temperature rules),
> **§4** (call_tag discipline), **§9** (timeout prevention), **§13** (Claude Opus 4.6 config).

---

## Step 0 — Decide If a Review Is Required

Review is **mandatory** (Strategy B — see `INFO_AI_RULES.md §0`) when:
- Auth / security / permissions / payment changes
- Database schema or migration changes
- Refactor > ~50 LOC or new core feature
- "I'm stuck" — agent cannot resolve independently
- Domain-expert validation (clinical, regulatory, taxonomy)

If none apply → Strategy A (internal reasoning only, skip this workflow).

---

## Step 1 — Choose Model

| Scenario | Model | Reference |
|---|---|---|
| Code review, architecture, general audit | **GPT-5.4** | `INFO_AI_RULES.md §1, §2a` |
| Domain expertise, taxonomy, field specs | **Claude Opus 4.6** | `INFO_AI_RULES.md §13` |
| Multi-part chained review (>3 parts) | **Claude Opus 4.6** | `INFO_AI_RULES.md §13` (caching) |
| Large file (Star Topology) | **GPT-5.4** | `INFO_AI_RULES.md §1` (Strategy B) |

---

## Step 2 — Construct `call_tag` (see `INFO_AI_RULES.md §4`)

```
REVIEW_<PROJECT>_<SCOPE>_<EFFORT>_<YYYYMMDD_HHMMSS>_IST
```

Star Topology branches: `_B01_L0001-0300_...`
Opus chained parts: `_OPUS46_PART2_...`, `_PART3_...`

---

## Step 3 — Create Review Script

**DO NOT write from scratch.** Copy the appropriate template and customize:

| Example file | Pattern | Reference |
|---|---|---|
| `temp/TEMP_review_gpt54_example.py` | GPT-5.4 single call + star topology | `INFO_AI_RULES.md §1, §9` |
| `temp/TEMP_review_opus46_chained_example.py` | Opus 4.6 multi-part with cache chain | `INFO_AI_RULES.md §13` |

**Key rules from INFO_AI_RULES (don't re-read the file — just follow these):**
- GPT-5.4: `reasoning={"effort": "high"}` (nested object — `INFO_AI_RULES.md §3`)
- GPT-5.4: `store=True` mandatory for star topology (`INFO_AI_RULES.md §1`)
- GPT-5.4: timeout 600s for high, 1200s for xhigh (`INFO_AI_RULES.md §9`)
- Opus 4.6: `max_tokens ≥ budget_tokens + expected_text` (`INFO_AI_RULES.md §13`)
- Opus 4.6: streaming mandatory for >10K output (`INFO_AI_RULES.md §13`)
- Opus 4.6: `cache_control` on content blocks, not messages (`INFO_AI_RULES.md §13`)
- API key: use `LLMClient` if available (`INFO_AI_RULES.md §8`)

Save script to: `temp/TEMP_review_<scope>_<part>.py`

---

## Step 4 — Run & Save Output

```
python temp/TEMP_review_<scope>.py
```

**Three outputs MUST be created:**
1. `DOCS/reviews/<CALL_TAG>.md` — Text response
2. `DOCS/reviews/<CALL_TAG>_THINKING.md` — Thinking trace (Opus only)
3. `DOCS/AGENT_API_TRACE.jsonl` — Append one JSONL line (see `INFO_AI_RULES.md §4.4`)

---

## Step 5 — Update Documentation

1. **`DOCS/CHANGE_LOG.md`** — Add entry with `call_tag`, `response_id`, what was decided
2. **`DOCS/AGENT_HANDOVER.md`** — Update if review affects active work
3. **`DOCS/AGENT_DECISIONS.md`** — Document if review changed a design decision