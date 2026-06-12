#!/usr/bin/env python3
"""
BEAM × Palest Ink — Agentic evaluation via OpenAI SDK.
"""

import json
import os
import sys
import glob as globmod
import subprocess
import time
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_TOKEN"],
)
MODEL = os.environ.get("MODEL", "mimo-v2.5")

SKILL_PATH = Path(__file__).resolve().parents[2] / "skills" / "palest-ink" / "SKILL.md"

# ── Tools ─────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read a file. Returns content with line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "offset": {"type": "integer", "description": "Start line (0-based)"},
                    "limit": {"type": "integer", "description": "Max lines"}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Write",
            "description": "Write content to a file. Creates dirs if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Edit",
            "description": "Replace text in a file. Use to append by replacing a marker at end of file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "old_string": {"type": "string"},
                    "new_string": {"type": "string"}
                },
                "required": ["file_path", "old_string", "new_string"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Glob",
            "description": "Find files matching a pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string"}
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Grep",
            "description": "Search for text in files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string"},
                    "include": {"type": "string"}
                },
                "required": ["pattern", "path"]
            }
        }
    },
]


def execute_tool(name, args):
    try:
        if name == "Read":
            p = Path(args["file_path"])
            if not p.exists():
                return f"Error: file not found: {args['file_path']}"
            lines = p.read_text().splitlines()
            offset = args.get("offset", 0)
            limit = args.get("limit", 2000)
            selected = lines[offset:offset + limit]
            return "\n".join(f"{i+offset+1}\t{line}" for i, line in enumerate(selected))

        elif name == "Write":
            p = Path(args["file_path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"])
            return f"Written {len(args['content'])} chars to {args['file_path']}"

        elif name == "Edit":
            p = Path(args["file_path"])
            if not p.exists():
                return f"Error: file not found: {args['file_path']}"
            content = p.read_text()
            if args["old_string"] not in content:
                return f"Error: old_string not found in {args['file_path']}"
            new_content = content.replace(args["old_string"], args["new_string"], 1)
            p.write_text(new_content)
            return f"Edited {args['file_path']}"

        elif name == "Glob":
            path = args.get("path", ".")
            matches = globmod.glob(os.path.join(path, args["pattern"]), recursive=True)
            return "\n".join(sorted(matches)) if matches else "No matches"

        elif name == "Grep":
            path = args["path"]
            cmd = ["grep", "-rn", args["pattern"], path]
            if "include" in args:
                cmd = ["grep", "-rn", "--include=" + args["include"], args["pattern"], path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout[:5000] if result.stdout else "No matches"

        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {e}"


def run_agent_turn(messages, max_rounds=30, label=""):
    """Tool-use loop with logging."""
    for round_i in range(max_rounds):
        for attempt in range(5):
            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0,
                    max_tokens=4096,
                )
                break
            except Exception as e:
                if "429" in str(e) and attempt < 4:
                    wait = 3 * (attempt + 1)
                    print(f"    [429] retry {attempt+1} in {wait}s", flush=True)
                    time.sleep(wait)
                else:
                    print(f"    [ERROR] {e}", flush=True)
                    raise

        msg = resp.choices[0].message
        messages.append(msg.model_dump())

        if not msg.tool_calls:
            # Final text response
            text = msg.content or ""
            if label and text:
                print(f"    [{label}] {text[:100]}...", flush=True)
            return text

        # Execute tool calls with logging
        for tc in msg.tool_calls:
            fn = tc.function.name
            args = json.loads(tc.function.arguments)
            fp = args.get("file_path", args.get("path", ""))
            short = str(fp).split("/")[-1] if fp else ""
            print(f"    [{label}] {fn}({short})", flush=True)

            result = execute_tool(fn, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result[:10000],
            })
        time.sleep(0.5)

    return "(max rounds)"


# ── Extraction ────────────────────────────────────────────────────

def run_extraction(chat_dir, chat_id):
    chat_dir = Path(chat_dir)
    ext_dir = chat_dir / "extraction"
    ext_dir.mkdir(parents=True, exist_ok=True)

    skill = SKILL_PATH.read_text()

    # Pre-create INK.md with standard structure
    (ext_dir / "INK.md").write_text("""# INK.md

## Conceptual
- conceptual/tech-stack.md
- conceptual/design-decisions.md

## Structural
- structural/project-structure.md
- structural/database-schema.md
- structural/dependencies.md

## Behavioral
- behavioral/auth-patterns.md
- behavioral/api-conventions.md
- behavioral/development-workflow.md

## Operational
- operational/project-timeline.md
- operational/dev-log.md
- operational/user-preferences.md
""")

    # Pre-create empty docs
    for rel in [
        "conceptual/tech-stack.md", "conceptual/design-decisions.md",
        "structural/project-structure.md", "structural/database-schema.md", "structural/dependencies.md",
        "behavioral/auth-patterns.md", "behavioral/api-conventions.md", "behavioral/development-workflow.md",
        "operational/project-timeline.md", "operational/dev-log.md", "operational/user-preferences.md",
    ]:
        p = ext_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text(f"# {rel.split('/')[-1].replace('.md','').replace('-',' ').title()}\n")

    # Determine project topic from first turn
    with open(chat_dir / "chat.json") as f:
        chat_data = json.load(f)

    first_msg = chat_data[0]["turns"][0][0]["content"][:200]

    system = f"""You are extracting knowledge from a long conversation into structured project documents.

{skill}

---

Context: This is a multi-turn conversation between a user and an assistant about building a software project. The conversation spans many turns with time anchors and turn IDs.

Working directory: {ext_dir}

A document structure (INK.md + 11 documents) is already set up. Your job:
1. Read INK.md to see the document map
2. As you receive conversation turns, read existing documents to understand what's already been captured
3. Extract new knowledge and update the appropriate document using Edit (append to the end)
4. If a topic doesn't fit any existing document, create a new one and update INK.md
5. Preserve time anchors (dates) and turn IDs in Operational documents
6. Don't duplicate — only add genuinely new information

This is a CONTINUOUS conversation. Read existing documents before updating to avoid duplication.
Prefer editing existing documents over creating new ones."""

    messages = [{"role": "system", "content": system}]

    all_turns = []
    for batch in chat_data:
        for turn in batch.get("turns", []):
            all_turns.append(turn)

    print(f"[{chat_id}] {len(all_turns)} turns", flush=True)

    # Feed in groups of 5 turns
    BATCH = 5
    for start in range(0, len(all_turns), BATCH):
        batch = all_turns[start:start + BATCH]
        text = ""
        for ti, turn in enumerate(batch, start=start):
            text += f"--- Turn {ti} ---\n"
            for msg in turn:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                tid = msg.get("index", "")
                ta = msg.get("time_anchor", "")
                meta = f" (time: {ta}, id: {tid})" if ta else ""
                text += f"[{role}]{meta}: {content}\n"
            text += "\n"

        messages.append({"role": "user", "content": text})
        end = min(start + BATCH, len(all_turns))
        run_agent_turn(messages, label=f"turns {start}-{end}")
        print(f"[{chat_id}] {end}/{len(all_turns)} turns done", flush=True)

    # Summary
    messages.append({"role": "user", "content": "All turns processed. Write a brief summary to summary.md."})
    run_agent_turn(messages, label="summary")

    docs = len(list(ext_dir.rglob("*.md")))
    print(f"[{chat_id}] done: {docs} documents", flush=True)


# ── Answering ─────────────────────────────────────────────────────

def run_answering(chat_dir, chat_id):
    chat_dir = Path(chat_dir)
    ext_dir = chat_dir / "extraction"
    answers_dir = chat_dir / "answers"
    logs_dir = chat_dir / "logs"
    answers_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    skill = SKILL_PATH.read_text()

    with open(chat_dir / "probing_questions.json") as f:
        probing = json.load(f)

    ink_path = str(ext_dir / "INK.md")
    system = f"""You are answering questions about a project using its Palest Ink documents.

{skill}

---

IMPORTANT: All project documents are under: {ext_dir}

- INK.md is at: {ink_path}
- Documents are in subdirectories: conceptual/, structural/, behavioral/, operational/
- Example: {ext_dir}/conceptual/tech-stack.md

For each question:
1. Read {ink_path} to see available documents
2. Decide which documents are relevant
3. Read ONLY those documents using their FULL paths
4. Answer based ONLY on the document content
5. If documents don't contain enough info, say so

Always use full absolute paths when calling Read."""

    all_answers = {}
    all_logs = {}

    for category, questions in probing.items():
        cat_answers = []
        cat_logs = {}

        for qi, q in enumerate(questions):
            q_key = f"Q{qi+1}"
            question = q["question"]

            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": f"Question ({category}): {question}"}
            ]

            answer = run_agent_turn(messages, label=f"{category}/{q_key}")

            # Extract files read
            files_read = []
            for m in messages:
                if m.get("role") == "assistant" and m.get("tool_calls"):
                    for tc in m["tool_calls"]:
                        if tc["function"]["name"] == "Read":
                            a = json.loads(tc["function"]["arguments"])
                            fp = a.get("file_path", "")
                            if fp and fp not in files_read:
                                files_read.append(fp)

            cat_answers.append({"question": question, "answer": answer})
            cat_logs[q_key] = files_read

        all_answers[category] = cat_answers
        all_logs[category] = cat_logs

    with open(answers_dir / "palest_ink_agentic.json", "w") as f:
        json.dump(all_answers, f, ensure_ascii=False, indent=2)
    with open(logs_dir / "palest_ink_agentic_files.json", "w") as f:
        json.dump(all_logs, f, ensure_ascii=False, indent=2)

    print(f"[{chat_id}] answering done", flush=True)


# ── Main ──────────────────────────────────────────────────────────

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "help"
    chat_ids = sys.argv[2:] if len(sys.argv) > 2 else ["1"]
    base = os.environ.get("BEAM_BASE", "/tmp/beam-100k-eval")

    if mode == "extract":
        for cid in chat_ids:
            d = f"{base}/chat-{cid}"
            if not os.path.exists(f"{d}/chat.json"):
                print(f"Chat {cid}: no chat.json")
                continue
            print(f"\n{'='*50}\nExtract chat-{cid}\n{'='*50}", flush=True)
            t = time.time()
            run_extraction(d, cid)
            print(f"[{cid}] {time.time()-t:.0f}s total\n", flush=True)

    elif mode == "answer":
        for cid in chat_ids:
            d = f"{base}/chat-{cid}"
            if not os.path.exists(f"{d}/extraction/INK.md"):
                print(f"Chat {cid}: no INK.md")
                continue
            print(f"\n{'='*50}\nAnswer chat-{cid}\n{'='*50}", flush=True)
            t = time.time()
            run_answering(d, cid)
            print(f"[{cid}] {time.time()-t:.0f}s total\n", flush=True)

    else:
        print("Usage: python beam_eval.py [extract|answer] [chat_ids...]")


if __name__ == "__main__":
    main()
