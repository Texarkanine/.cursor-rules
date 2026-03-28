---
description: Guidance for writing batch scripts to replace repetitive tool call loops — covers discovering available runtimes and CLI tools, choosing the right scripting approach, and structuring efficient collect-then-reason workflows
globs:
alwaysApply: false
---

# Batch Scripting Instead of Tool Call Loops

You're here because you recognized you were about to loop tool calls over a mechanical operation. Good. This skill helps you write the script that replaces the loop.

## Step 1: Know What You Have

Before writing a script, confirm what the environment provides. Don't inventory everything — check what you need for the task at hand.

**Assume nothing about the platform.** POSIX baseline tools (`grep`, `awk`, `sed`, `find`, `sort`, `diff`, `xargs`, `cut`, `wc`, `head`, `tail`, `tee`) are available on Unix-like systems but not on Windows. When the platform is ambiguous, verify before depending on them.

**Check runtimes, not individual tools.** The critical question is "which language runtimes are present?" — not "which CLI tools are installed." A runtime unlocks its entire standard library, and you already know from training what those standard libraries contain. A single `python3 --version` check unlocks `json`, `csv`, `re`, `pathlib`, `glob`, `subprocess`, `tempfile`, `difflib`, `collections.Counter`, `xml.etree`, `sqlite3`, `http.client`, `shutil`, and more. A single `node --version` check unlocks `fs`, `path`, `child_process`, `JSON`, `os`, `url`, `readline`, `crypto`, `zlib`.

**Enhanced CLI tools are a bonus.** If a purpose-built tool (a JSON processor, a fast search tool, a tree visualizer, a YAML processor, a language-specific package manager CLI) would make the script meaningfully simpler, check for it before using it. If it's there, use it. If not, fall back to the runtime stdlib that covers the same capability. **Never install tools to satisfy this optimization.** Use what exists.

**If you need to check multiple things, check them in one tool call.** Write a small probe that tests for everything you need in a single execution. Don't fall into the very anti-pattern that brought you here by checking tools one at a time.

## Step 2: Choose Your Approach

**Decision order:**

1. **Can a shell pipeline handle this?** Simple filtering, counting, sorting, deduplication, file-finding — baseline shell tools handle these without needing a runtime. A `grep | sort | uniq -c` pipeline is often the whole answer.

2. **Does this involve structured data (JSON, CSV, XML, YAML) or logic with branching/error handling?** Confirm a runtime is available, then use its stdlib. Python is the strongest general-purpose fallback — its stdlib covers nearly every data format and operation. Node is strong when the task is JSON-centric or the project is already JavaScript/TypeScript.

3. **Would a specialized CLI tool cut the script from 15 lines to 1?** Check if it's available. Use it if present. If not, the runtime approach from step 2 still works — it's just slightly more verbose.

**Stdlib-only constraint:** Do not import external packages. No `pip install`, no `npm install`, no `gem install`. If a capability isn't in the runtime's standard library, either use a different approach or accept the slightly-less-elegant shell version. The goal is zero setup cost.

## Step 3: Write the Script

**Structure every batch script the same way:**

1. **Collect** — iterate over the inputs, call APIs/read files/query databases in batch where possible, extract only the fields you'll need for reasoning
2. **Compress** — reduce verbose outputs to just the relevant data; don't dump 4KB of JSON when you need 3 fields
3. **Output to a tempfile** — write consolidated results somewhere stable that can be re-read later without re-executing

**Batch-first I/O:** Prefer bulk operations over iteration. GraphQL over per-resource REST. `--paginate` flags over manual page-following. `find -exec` over per-file tool calls. `SELECT ... FROM information_schema` over per-table `DESCRIBE`. Multi-key queries over single-key lookups.

**Compression matters.** Raw API responses, full file contents, and verbose command outputs burn context window when read back. The script should extract, filter, and format before writing the output file. The reasoning step that follows should receive a clean, minimal dataset — not raw firehose output.

## Step 4: Execute and Read

Two tool calls:
1. **Execute the script.** One invocation that runs the full batch.
2. **Read the tempfile.** One read of the consolidated, compressed output.

If you need to re-examine the data later in the conversation, re-read the tempfile. Don't re-collect.

## Recognizing Common Shapes

These situations all share the same structure — a loop that should be a script:

- **Serial API calls** over a list of resources when a batch endpoint, paginated fetch-all, or query language (GraphQL, SQL) exists
- **Opening files one-by-one** to search for content that a search tool can locate in one pass
- **Walking API pagination** by fetching each page as a separate tool call instead of scripting the cursor-following loop
- **Data format conversion** (CSV↔JSON, field extraction, restructuring) that any data-processing runtime handles natively
- **Generating N similar files** from a template with variable substitution
- **Collecting environment info** (versions, paths, configurations) one command per tool call
- **Traversing dependency trees, database schemas, or directory structures** that a single query or command already exposes in full
- **Diffing or comparing** by reading both sides into context and eyeballing, instead of using a diff tool
- **Filtering logs or output** by reading large files into context and scanning, instead of letting a filter tool extract matches

In every case, the diagnostic question is the same: **between step N and step N+1, does the agent need to understand language to decide what to do next?** If the next step is mechanically derivable from the current step's output — if it's just incrementing through a list — it's a for-loop, and it belongs in a script.
