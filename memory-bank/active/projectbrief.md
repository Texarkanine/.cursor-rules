# Project Brief: PR Feedback Judge Command

## User Story

As a developer who frequently asks an AI agent to evaluate pull-request review feedback (typically at the `reflect → pr open → [here]` point of a Niko flow), I want a single Cursor command that takes one or more GitHub PR-feedback URLs and produces a per-item "valid or invalid" verdict using my standard questioning/evaluation intro — so I stop hand-pasting the same framing every time.

## Requirements

### Inputs
The command must accept a free mix of these URL shapes, in any combination, in a single invocation:

1. **Whole PR** — `https://github.com/<owner>/<repo>/pull/<N>` → evaluate every piece of review feedback on the PR.
2. **PR review** — `https://github.com/<owner>/<repo>/pull/<N>#pullrequestreview-<id>` → evaluate every comment that belongs to that specific review.
3. **Single comment** — any of:
   - `#discussion_r<id>` (inline review comment, may or may not be part of a review)
   - `#issuecomment-<id>` (standalone PR-conversation comment)
   - other comment anchors that resolve to a single comment
   → evaluate just that one comment.

### Behavior
- Apply the user's standard questioning/evaluation intro (the "valid or invalid" framing seeded by `memory-bank/cursor_pull_request_feedback_references.md`); formalize the exact wording as part of this task.
- Render a per-item verdict for each URL provided.
- Batch-fetch GitHub data (per `script-it-instead`) — never N tool calls for N comments.

### Packaging
- Ship as a **ruleset** under `rulesets/` (canonical source per `agent-customization-locations`), not as a standalone rule.
- The ruleset composes `script-it-instead` so consumers who already include it don't get duplicate content.
- The ruleset installs into both `.cursor/` and `.claude/` ecosystems via the existing `ai-rizz` / `a16n` toolchain.

### Out of Scope (Explicitly)
- **`/nk-chat` / `/nk-with`** ([issue #63](https://github.com/Texarkanine/.cursor-rules/issues/63)). The Niko-context coupling problem is real but will be solved separately in a different thread; we will be rebased onto its result. This task assumes the command runs either inside a live Niko conversation or context-free, and does not try to load the memory bank itself.
- Verdict-tracking persistence (the command renders verdicts to chat; it does not write them to the memory bank).

## Open Design Questions (for Creative Phase)

1. **GitHub access strategy.** Inventory what's actually available in this environment — `gh` CLI, a GitHub MCP server, raw `curl`, Cursor's URL pre-fetch (noisy HTML) — and pick the path that returns just the comment body + author + diff context with minimal noise. Then design the batch-fetch script shape.
2. **Verdict / intro template.** Pin down the exact "valid or invalid" intro and per-item verdict format the command injects.
3. **URL parsing & dispatch.** How the command classifies an input URL into one of the three shapes and chooses the right fetch + evaluation path.
