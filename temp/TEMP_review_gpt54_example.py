"""
TEMPLATE: GPT-5.4 Review — Single Call + Star Topology
========================================================
Copy this file to temp/TEMP_review_<scope>.py and customize.

Patterns covered:
  A) Single high-reasoning review
  B) Star Topology (root + parallel branches for large files)

Reference: DOCS/INFO_AI_RULES.md Sections 1, 2a, 3, 9
"""

import os, json, datetime, asyncio

# ============================================================================
# CONFIG — Customize these for your project
# ============================================================================

# API Key — Use LLMClient if available, else env var, else secrets.json
try:
    from llm_client import LLMClient
    API_KEY = LLMClient().api_key
except ImportError:
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        with open("secrets.json") as f:
            API_KEY = json.load(f).get("OPENAI_API_KEY")

MODEL = "gpt-5.4"
REASONING_EFFORT = "high"       # "none" | "medium" | "high" | "xhigh"
TIMEOUT = 600.0                 # 10 min for high; 1200 for xhigh

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PROJECT = "MYAPP"               # ← Change to your project name
SCOPE = "ARCH_REVIEW"           # ← Change to your review scope
CALL_TAG = f"REVIEW_{PROJECT}_{SCOPE}_{REASONING_EFFORT.upper()}_{TIMESTAMP}_IST"

OUTPUT_DIR = os.path.join("DOCS", "reviews")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
# PATTERN A: Single High-Reasoning Review
# ============================================================================

def run_single_review():
    """
    Simple one-shot review. Use for:
    - Code audits < 1M tokens of context
    - Architecture reviews
    - Security reviews
    """
    from openai import OpenAI

    client = OpenAI(api_key=API_KEY, timeout=TIMEOUT)

    # ── Build your prompt ──
    prompt = f"""
    [VERBOSITY: HIGH]

    You are a senior software architect reviewing a codebase for [SCOPE].

    ## CONTEXT
    [Paste your code, architecture docs, or file contents here]

    ## YOUR TASK
    [Describe exactly what you want reviewed]

    ## OUTPUT FORMAT
    Structure your response as:
    ### Critical Issues
    ### Recommendations
    ### Summary
    """

    print(f"🚀 Sending review: {CALL_TAG}")
    print(f"   Model: {MODEL} | Reasoning: {REASONING_EFFORT}")

    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": REASONING_EFFORT},   # Nested object — MANDATORY
        input=prompt,
        store=True,                                 # MANDATORY for caching
    )

    # ── Save output ──
    out_file = os.path.join(OUTPUT_DIR, CALL_TAG + ".md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"# GPT-5.4 Review: {SCOPE}\n\n")
        f.write(f"*Model: {MODEL} | Reasoning: {REASONING_EFFORT}*\n")
        f.write(f"*Response ID: {response.id}*\n\n---\n\n")
        f.write(response.output_text)

    # ── Trace log ──
    _append_trace(response.id, None)

    print(f"✅ Saved to: {out_file}")
    print(f"   Response ID: {response.id}")


# ============================================================================
# PATTERN B: Star Topology (Root + Parallel Branches)
# ============================================================================

def chunk_file(file_path, chunk_size=300):
    """Split a file into chunks for parallel review."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    chunks = []
    for i in range(0, len(lines), chunk_size):
        segment = "".join(lines[i:i + chunk_size])
        chunks.append({
            "index": i // chunk_size + 1,
            "start_line": i + 1,
            "end_line": min(i + chunk_size, len(lines)),
            "content": segment
        })
    return chunks


async def run_star_topology(file_path):
    """
    Star Topology review for large files.
    Root establishes context, branches review chunks in parallel.
    Each branch gets the cached root context at 90% discount.
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=API_KEY, timeout=TIMEOUT)

    # ── Step 1: Root context (no code, just instructions) ──
    root_prompt = """
    You are a Security Architect reviewing a large codebase file.

    ## GLOBAL RULES
    - No raw SQL, no hardcoded secrets, verify all inputs
    - Focus on: logic errors, security flaws, bad practices

    ## CONTEXT
    I will send you segments of the file. Review each in isolation.

    ## OUTPUT FORMAT (JSON)
    {"critical_issues": [], "suggestions": []}

    ## NOTE
    You are reviewing a FRAGMENT. Do not flag 'undefined variables' or
    'missing imports' — they may be defined in other segments.
    """

    print("🌱 Creating Root Context...")
    root = await client.responses.create(
        model=MODEL,
        input=root_prompt,
        store=True   # MANDATORY for star topology
    )
    ROOT_ID = root.id
    print(f"✅ Root established: {ROOT_ID}")

    # ── Step 2: Fork branches from root (parallel) ──
    chunks = chunk_file(file_path, chunk_size=200)
    print(f"📂 Split into {len(chunks)} branches")

    semaphore = asyncio.Semaphore(5)  # Rate limit

    async def review_chunk(chunk):
        async with semaphore:
            branch_tag = f"REVIEW_{PROJECT}_{SCOPE}_B{chunk['index']:02d}_L{chunk['start_line']:04d}-{chunk['end_line']:04d}_{TIMESTAMP}_IST"
            print(f"   👉 Branch {chunk['index']} (Lines {chunk['start_line']}-{chunk['end_line']})...")

            resp = await client.responses.create(
                model=MODEL,
                reasoning={"effort": REASONING_EFFORT},
                previous_response_id=ROOT_ID,   # ← Cached root context (90% discount)
                input=f"""
                ## SEGMENT REVIEW
                Lines: {chunk['start_line']} to {chunk['end_line']}

                ```python
                {chunk['content']}
                ```
                """,
                store=True,
            )
            return {
                "branch_tag": branch_tag,
                "chunk": chunk["index"],
                "lines": f"{chunk['start_line']}-{chunk['end_line']}",
                "response_id": resp.id,
                "analysis": resp.output_text,
            }

    results = await asyncio.gather(*[review_chunk(c) for c in chunks])

    # ── Step 3: Save results ──
    for res in results:
        out_file = os.path.join(OUTPUT_DIR, res["branch_tag"] + ".md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"# GPT-5.4 Star Branch: Lines {res['lines']}\n\n")
            f.write(f"*Response ID: {res['response_id']}*\n")
            f.write(f"*Root ID: {ROOT_ID}*\n\n---\n\n")
            f.write(res["analysis"])
        _append_trace(res["response_id"], ROOT_ID)

    print(f"\n🏁 Star topology complete. {len(results)} branches reviewed.")


# ============================================================================
# TRACE LOGGER
# ============================================================================

def _append_trace(response_id, previous_id):
    """Append a JSONL trace entry to DOCS/AGENT_API_TRACE.jsonl"""
    trace = {
        "timestamp": datetime.datetime.now().isoformat(),
        "call_tag": CALL_TAG,
        "response_id": response_id,
        "previous_response_id": previous_id,
        "model": MODEL,
        "reasoning": {"effort": REASONING_EFFORT},
        "agent": "Architect",
        "success": True,
    }
    trace_path = os.path.join("DOCS", "AGENT_API_TRACE.jsonl")
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(trace) + "\n")


# ============================================================================
# MAIN — Choose which pattern to run
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--star":
        # Star topology: python TEMPLATE_review_gpt54.py --star path/to/file.py
        target = sys.argv[2] if len(sys.argv) > 2 else "src/large_file.py"
        asyncio.run(run_star_topology(target))
    else:
        # Single review
        run_single_review()
