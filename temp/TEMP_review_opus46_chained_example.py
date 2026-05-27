"""
TEMPLATE: Claude Opus 4.6 — Multi-Part Chained Review with Prompt Caching
===========================================================================
Copy this file to temp/TEMP_review_opus46_<scope>_part<N>.py and customize.

Patterns covered:
  A) Single-call review with extended thinking
  B) Multi-part chained review with prompt caching (Parts 1→2→...→N)

Reference: DOCS/INFO_AI_RULES.md Section 13 (all subsections)

TOKEN STRATEGY (Section 13.5):
  max_tokens = budget_tokens + expected_text_output
  - Long text output → budget LOW (8K-16K), max_tokens HIGH (64K-128K)
  - Deep reasoning   → budget HIGH (32K-100K), accept shorter text
  - NEVER set max_tokens == budget_tokens (leaves zero room for text)

CACHE STRATEGY (Section 13.6):
  - cache_control goes on content BLOCKS, not messages
  - Cache the LARGEST blocks that repeat across parts
  - Cache has 5-minute TTL — run parts quickly or accept re-creation
  - Minimum 1,024 tokens per cached block
"""

import os, sys, json, datetime, glob
import anthropic

# ============================================================================
# CONFIG — Customize these for your project
# ============================================================================

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-ant-...")

MODEL = "claude-opus-4-6"
BUDGET_TOKENS = 32_000     # Thinking budget (see token strategy above)
MAX_TOKENS = 64_000        # Output limit = budget + expected text

TIMESTAMP_IST = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PROJECT = "MYAPP"          # ← Change to your project name
SCOPE = "ARCH_REVIEW"      # ← Change to your review scope
PART_NUM = 1               # ← Change for each part (1, 2, 3, ...)

if PART_NUM == 1:
    CALL_TAG = f"REVIEW_{PROJECT}_{SCOPE}_OPUS46_{TIMESTAMP_IST}_IST"
else:
    CALL_TAG = f"REVIEW_{PROJECT}_{SCOPE}_OPUS46_PART{PART_NUM}_{TIMESTAMP_IST}_IST"

OUTPUT_DIR = os.path.join("DOCS", "reviews")
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
    timeout=1200.0,    # 20 minutes — Opus thinking is SLOW
    max_retries=2
)


# ============================================================================
# PATTERN A: Single-Call Review (Part 1 or Standalone)
# ============================================================================

def build_single_call_messages():
    """
    Build messages for a standalone or Part 1 review.
    Put cache_control on the largest content block.
    """

    # ── Load your context (code files, prior review output, etc.) ──
    context_files = {}
    files_to_read = [
        # ("label", "path/to/file.py"),
        # Add your files here
    ]
    for label, path in files_to_read:
        try:
            with open(path, "r", encoding="utf-8") as f:
                context_files[label] = f.read()
        except FileNotFoundError:
            context_files[label] = f"# FILE NOT FOUND: {path}"

    code_context = ""
    for label, content in context_files.items():
        code_context += f"\n\n### {label}\n```python\n{content}\n```\n"

    # ── Build the prompt ──
    prompt = f"""You are a senior [DOMAIN] expert with 20+ years of experience.

## YOUR TASK
[Describe your review task in detail]

## CONTEXT
{code_context if code_context else "[Paste your context here]"}

## OUTPUT FORMAT
Structure your response as:
### Findings
### Recommendations
### Summary

Be direct and practical.
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                    "cache_control": {"type": "ephemeral"}  # Cache the large context
                }
            ]
        }
    ]

    return messages


# ============================================================================
# PATTERN B: Multi-Part Chained Review (Part 2, 3, ... N)
# ============================================================================

def build_chained_messages():
    """
    Build messages for Part N of a chained review.

    HOW IT WORKS:
    1. Reconstruct the EXACT prompts from prior parts (byte-for-byte for cache hits)
    2. Load saved responses from prior parts
    3. Build the full message chain: [user1, assistant1, user2, assistant2, ..., userN]
    4. Put cache_control on the largest blocks

    CRITICAL:
    - Prior prompts must be EXACTLY the same text as when they were first sent
    - Store prompts as variables or read from saved scripts
    - If the text differs by even 1 character, cache will miss
    """

    # ── Step 1: Reconstruct prior prompts ──
    # Option A: Hardcode the exact prompts (most reliable for cache hits)
    PART_1_PROMPT = "..."   # ← Paste the exact Part 1 prompt here

    # Option B: Read from prior script files (extract the prompt variable)
    # with open("temp/TEMP_review_opus46_<scope>_part1.py", "r") as f:
    #     ... parse out the prompt ...

    # ── Step 2: Load saved responses ──
    def find_latest_review(pattern):
        """Find the most recent review output matching a glob pattern."""
        candidates = sorted(glob.glob(os.path.join(OUTPUT_DIR, pattern)))
        candidates = [p for p in candidates if "_THINKING" not in p]
        if not candidates:
            print(f"ERROR: No file matching {pattern}")
            sys.exit(1)
        return candidates[-1]

    part1_response_path = find_latest_review(f"REVIEW_{PROJECT}_{SCOPE}_OPUS46_*_IST.md")
    with open(part1_response_path, "r", encoding="utf-8") as f:
        PART1_RESPONSE = f.read()
    print(f"Loaded Part 1 response: {part1_response_path}")

    # For Part 3+, also load Part 2 response:
    # part2_response_path = find_latest_review(f"REVIEW_{PROJECT}_{SCOPE}_OPUS46_PART2_*_IST.md")
    # with open(part2_response_path, "r") as f:
    #     PART2_RESPONSE = f.read()

    # ── Step 3: New prompt for this part ──
    NEW_PROMPT = f"""## PART {PART_NUM}: [Your new task title]

[Your detailed prompt for this part]
"""

    # ── Step 4: Build the message chain ──
    messages = [
        # Part 1: user prompt (CACHED — largest block)
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": PART_1_PROMPT,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        },
        # Part 1: assistant response
        {
            "role": "assistant",
            "content": PART1_RESPONSE
        },
        # Part 2+ prompts and responses go here...
        # {
        #     "role": "user",
        #     "content": PART_2_PROMPT
        # },
        # {
        #     "role": "assistant",
        #     "content": [
        #         {"type": "text", "text": PART2_RESPONSE, "cache_control": {"type": "ephemeral"}}
        #     ]
        # },

        # New prompt for THIS part (no cache — it's the new content)
        {
            "role": "user",
            "content": NEW_PROMPT
        }
    ]

    return messages


# ============================================================================
# SEND, EXTRACT, SAVE, TRACE
# ============================================================================

def run_review():
    """Run the review with streaming, save output and thinking, log trace."""

    # Choose pattern based on part number
    if PART_NUM == 1:
        messages = build_single_call_messages()
    else:
        messages = build_chained_messages()

    # ── Print summary ──
    print("=" * 70)
    print(f"CLAUDE OPUS 4.6 — Part {PART_NUM}")
    print(f"Call tag:       {CALL_TAG}")
    print(f"Model:          {MODEL}")
    print(f"Budget tokens:  {BUDGET_TOKENS:,}")
    print(f"Max tokens:     {MAX_TOKENS:,}")
    print("=" * 70)
    total_chars = sum(len(str(m.get("content", ""))) for m in messages)
    print(f"Total context:  ~{total_chars:,} chars")
    print("Sending...")

    # ── Stream the response ──
    try:
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={
                "type": "enabled",
                "budget_tokens": BUDGET_TOKENS
            },
            messages=messages
        ) as stream:
            print("Stream connected, receiving response...")
            response = stream.get_final_message()
    except Exception as e:
        print(f"\n❌ API call failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # ── Extract thinking vs text ──
    thinking_text = []
    response_text = []
    for block in response.content:
        if block.type == "thinking":
            thinking_text.append(block.thinking)
        elif block.type == "text":
            response_text.append(block.text)

    content = "\n".join(response_text)
    thinking = "\n".join(thinking_text)
    msg_id = response.id

    # ── Read usage stats (including cache) ──
    usage = response.usage
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    cache_creation = getattr(usage, "cache_creation_input_tokens", 0)
    cache_read = getattr(usage, "cache_read_input_tokens", 0)

    # ── Check for truncation ──
    if response.stop_reason == "max_tokens":
        print("\n⚠️  WARNING: Output was TRUNCATED (stop_reason='max_tokens')!")
        print(f"   Increase max_tokens (currently {MAX_TOKENS:,}) or reduce prompt scope.")
    elif response.stop_reason == "end_turn":
        print("\n✅ Response completed successfully (stop_reason='end_turn')")

    # ── Save response ──
    out_file = os.path.join(OUTPUT_DIR, CALL_TAG + ".md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# Claude Opus 4.6 — Part {PART_NUM}: {SCOPE}\n\n")
        f.write(f"*Model: {MODEL} | Budget: {BUDGET_TOKENS:,} thinking tokens*\n")
        f.write(f"*Message ID: {msg_id}*\n")
        f.write(f"*Input: {input_tokens:,} tokens (Cache read: {cache_read:,}, "
                f"Cache creation: {cache_creation:,}) | Output: {output_tokens:,} tokens*\n\n")
        f.write("---\n\n")
        f.write(content)

    # ── Save thinking trace ──
    thinking_file = os.path.join(OUTPUT_DIR, CALL_TAG + "_THINKING.md")
    with open(thinking_file, "w", encoding="utf-8") as f:
        f.write(f"# Claude Opus 4.6 — Extended Thinking (Part {PART_NUM})\n\n")
        f.write(f"*Message ID: {msg_id}*\n\n---\n\n")
        f.write(thinking if thinking else "(No thinking content captured)")

    # ── Append trace to AGENT_API_TRACE.jsonl ──
    trace_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "call_tag": CALL_TAG,
        "response_id": msg_id,
        "model": MODEL,
        "thinking": {"budget_tokens": BUDGET_TOKENS},
        "input_tokens": input_tokens,
        "cache_read_tokens": cache_read,
        "cache_creation_tokens": cache_creation,
        "output_tokens": output_tokens,
        "agent": "Architect",
        "success": True,
        "label": f"Opus 4.6 Part {PART_NUM} ({SCOPE})"
    }
    trace_path = os.path.join("DOCS", "AGENT_API_TRACE.jsonl")
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(trace_entry) + "\n")

    # ── Final summary ──
    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)
    print(f"Saved to:       {out_file}")
    print(f"Thinking to:    {thinking_file}")
    print(f"Message ID:     {msg_id}")
    print(f"Input tokens:   {input_tokens:,}")
    print(f"Cache read:     {cache_read:,} (90% discount)")
    print(f"Cache creation: {cache_creation:,} (1.25× cost)")
    print(f"Output tokens:  {output_tokens:,}")
    if cache_read > 0:
        savings = (cache_read * 13.50) / 1_000_000  # $15-$1.50 saved per M tokens
        print(f"💰 Est. cache savings: ~${savings:.2f}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    run_review()
