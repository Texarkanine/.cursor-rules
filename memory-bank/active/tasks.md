# Task: PR Feedback Judge Command

* Task ID: pr-feedback-judge
* Complexity: Level 3
* Type: feature (new top-level command)

Build a Cursor slash command — `/pr-feedback-judge` — that takes one or more GitHub PR-feedback URLs (whole PR, PR review, or single comment in any combination) and renders per-item verdicts answering three questions (valid? worth fixing? in scope for this PR?) with an explicit disposition. Shipped as a single top-level `.md` command file under `rules/`, matching the `wiggum-niko-coderabbit-pr.md` convention. No ruleset wrapper — `script-it-instead` composition was reconsidered and determined to be over-engineering given the command's typical 1–3-item fetch profile; batch-fetch guidance specific to this command's fetch step is inlined in the command body instead.

## Pinned Info

### URL Shape → GitHub API Endpoint

The command's dispatch logic depends entirely on classifying input URLs. This table is the contract. The API path applies to the `gh` tier (T1, preferred); the GitHub MCP tier (T2, fallback) uses self-describing MCP tools whose schemas the agent reads at runtime.

| URL fragment | Shape | API path (under `https://api.github.com`) | Yields |
|---|---|---|---|
| (none) — `…/pull/N` | Whole PR | `/repos/{o}/{r}/pulls/{N}/comments` + `/repos/{o}/{r}/issues/{N}/comments` + `/repos/{o}/{r}/pulls/{N}/reviews` (all paginated) | Every inline review comment, every conversation comment, every review body |
| `#pullrequestreview-<rid>` | PR review | `/repos/{o}/{r}/pulls/{N}/reviews/<rid>` + `/repos/{o}/{r}/pulls/{N}/reviews/<rid>/comments` | Review body + every inline comment in that review |
| `#discussion_r<cid>` | Inline review comment | `/repos/{o}/{r}/pulls/comments/<cid>` | Single inline comment (incl. `diff_hunk`, `path`, `in_reply_to_id`) |
| `#issuecomment-<cid>` | Conversation comment | `/repos/{o}/{r}/issues/comments/<cid>` | Single conversation comment |

```mermaid
flowchart LR
    URL([User-supplied URL]) --> Classify{Fragment?}
    Classify -->|none| Whole["Whole PR<br/>3× paginated calls"]
    Classify -->|#pullrequestreview-N| Review["PR Review<br/>2× calls"]
    Classify -->|#discussion_r N| Inline["Inline comment<br/>1× call"]
    Classify -->|#issuecomment-N| Conv["Conversation comment<br/>1× call"]
    Whole & Review & Inline & Conv --> Norm["Normalize → flat list of items<br/>(author, body, path?, diff_hunk?, url)"]
    Norm --> Eval["Per-item evaluation using intro/verdict template"]
    Eval --> Render["Rendered verdict report"]
```

## Component Analysis

### Affected Components

- **`rules/pr-feedback-judge.md`** (NEW, sole deliverable): canonical command body. Lives top-level in `rules/` matching the `wiggum-niko-coderabbit-pr.md` convention. ai-rizz auto-registers top-level `rules/*.md` files as slash commands (syncs to `.cursor/commands/shared/<name>.md`). Contains the grounded questioning intro, URL-classification rubric, tier-detection block, per-tier fetch recipes, per-item verdict format, inlined batch-fetch guidance, failure-mode handling, and one example invocation.

### Cross-Module Dependencies

- **No source-tree dependencies.** The command body is self-contained — no symlinks into or out of any ruleset, no reference to `rulesets/script-it/` or similar.
- **Runtime dependencies** (the agent's environment when the command runs): one of, in priority order — `gh` CLI authenticated (T1, preferred — direct single-comment lookups), or a registered GitHub MCP server (T2, fallback — list-and-filter for single-comment URLs). Anonymous access cut. See Q2 creative doc.

### Boundary Changes

- **New public surface**: `/pr-feedback-judge <url>...` slash command becomes available via `ai-rizz add rule pr-feedback-judge` (single install path — no ruleset alternative).
- No existing rule, ruleset, skill, or command changes shape.

### Invariants & Constraints

1. **Canonical-source rule**: the command body MUST be edited only at `rules/pr-feedback-judge.md` (per `agent-customization-locations.mdc`). Any `.cursor/` or `.claude/` copies are downstream of `ai-rizz` / `a16n` sync.
2. **Inlined batch-fetch discipline**: the command body MUST include a fetch-step-specific instruction telling the agent to collapse 3+ structurally-identical `gh api` calls into a single batched script invocation. This replaces the previously-planned always-on `script-it-instead` dependency (dropped because the command's typical ask is 1–3 items, below the `script-it-instead` threshold; the inlined instruction is more targeted).
3. **No runtime persistence**: the command renders verdicts to chat and does not write to the memory bank.
4. **No Niko coupling**: the command MUST work both inside and outside a live Niko conversation. Memory-bank-context loading is `/nk-chat`'s job (issue #63, separate thread).

## Open Questions

- [x] **Q1 — Questioning intro & per-item verdict template (v0).** Provisionally resolved during plan-phase creative as scaffolded intro + hybrid (triage-table + valid-detail) verdict. Operator flagged the grounding (a summary doc only, not the actual user-prompt corpus) as insufficient. v0 is preserved in `creative-pr-feedback-judge-template.md` for design-history reasons but is **superseded by Q3** (see below). The v0 doc has a banner pointing at the grounded version.
- [x] **Q2 — GitHub fetch tier strategy.** Reopened three times. Final resolution: **T1 (`gh` CLI authenticated, preferred — direct single-comment lookups) → T2 (GitHub MCP, loose-detected by case-insensitive `github` substring match against MCP server name/identifier/description; agent reads tool schemas at runtime) → fail loudly**. Anonymous access cut. No env-var token harvesting. No sanity-check. Verified the popular `user-github` MCP exposes only PR/issue-scoped method-dispatch tools (no single-comment-by-ID getter), which is why T1 wins on efficiency. See `memory-bank/active/creative/creative-pr-feedback-judge-fetch-tiers.md`.
- [x] **Q3 — Questioning intro & per-item verdict template (grounded).** Promoted from a build step to its own creative exploration per operator: this is the real meat of the prompt design. Mined the actual user-prompt corpus from the local Cursor warehouse (21 URL-bearing user messages extracted, 12 clean signal). Findings: the user's actual criteria vocabulary is **valid / worth fixing / in scope for this PR**; the user wants the three questions answered separately; the user wants an explicit disposition (fix-now / defer-follow-up / dismiss); real ask sizes are 1–3 items so the triage table demotes to >5-items-only; corpus shows a failure mode where the agent answered before fetching the linked comment, requiring a load-bearing "fetch first" instruction. Final template in `memory-bank/active/creative/creative-pr-feedback-judge-template-grounded.md`.
- [x] **Q4 — Packaging: ruleset vs single rule.** Resolved during preflight. Originally planned as a ruleset (`rulesets/pr-feedback-judge/`) bundling `script-it-instead` via symlinks. Reconsidered: mapped the command's fetch mechanics to `script-it-instead`'s "third structurally-similar call" threshold against the corpus-grounded real-ask-size (median 2, mode 1). Threshold trips only when the user provides 3+ single-comment URLs of the same anchor type — a minority case. Conclusion: bundling an always-on rule for a sometimes-triggered batch case is over-engineering. Collapsed to a single top-level `rules/pr-feedback-judge.md` with the batch-fetch guidance inlined in the command body (targeted to the fetch step specifically, rather than always-on).

(URL parsing/dispatch was flagged as open in the projectbrief but collapsed: regex on the URL fragment, mapping unambiguous and now in the Pinned Info table.)

## Test Plan (TDD)

### Behaviors to Verify

This is a documentation/rule repo with no automated test framework (confirmed: no `tests/`, `test/`, `package.json`, or `Makefile`). "Tests" are inspection-grade validations. Each behavior maps to one mechanical check.

**Registration**

- B1: `rules/pr-feedback-judge.md` exists as a regular file (not a symlink).
- B2: `ai-rizz list` shows `/pr-feedback-judge` under "Available commands" (after push to remote — ai-rizz reads remote per `techContext.md`).

**Command-body well-formedness**

- B6: `rules/pr-feedback-judge.md` parses as Markdown without lint errors (visual review; no repo-wide markdown linter configured).
- B7: The command body documents all four URL shapes from the Pinned Info table.
- B8: The command body specifies the **tier-detection block in priority order T1 (`gh`) → T2 (GitHub MCP, loose-detected) → fail** and shows the `gh api` invocations for each URL shape; for T2, describes the access pattern (which logical operation per URL shape) without hardcoding MCP tool names.
- B9: The command body includes the grounded intro and per-item block from Q3 verbatim (intro + per-item block always; triage table conditional on >5 items).
- B10: The command body includes the inlined batch-fetch instruction: "if you end up with 3+ structurally-identical `gh api` calls in one invocation (e.g., multiple `#discussion_r…` URLs), issue them as one batched pipeline, not a sequential loop."
- B10a: The command body documents the failure modes from Q2: 404 in T1 → "private or deleted or malformed"; no tier available → "install gh and run gh auth login, or register a GitHub MCP server."
- B10b: The command body includes the load-bearing "fetch first, never judge from the URL alone" instruction from Q3 finding F6.

**Behavioral (manual smoke test)**

- B11: Pasting a real PR URL (e.g. `https://github.com/Texarkanine/a16n/pull/97`) plus a real `#discussion_r…` URL into a fresh chat with the command attached produces: one verdict per inline-review comment + one verdict per conversation comment + one verdict for the single inline comment, with no duplicate evaluations.
- B11a: Repeat B11 in a tier-degraded environment (`PATH` stripped of `gh`) — the command must still produce a correct rendering via T2 (GitHub MCP).
- B11b: Repeat B11 with neither `gh` nor a registered GitHub MCP — the command must surface the "install gh / register MCP" message rather than misclassifying or crashing or trying to fetch anonymously.
- B12: An invalid / malformed URL produces a clear "could not classify" message, not a crash.

(B3/B4/B5 dropped — they were ruleset-specific.)

### Test Infrastructure

- **Framework**: none formally; this repo treats inspection + manual smoke as the test plane.
- **Test location**: N/A.
- **Conventions**: shell one-liners for B1 and B7–B10b; visual review for B6; live chat invocation for B11–B12.
- **New test files**: none. The validation procedure goes inline in the QA-phase commands.

### Integration Tests

- B11/B12 are the integration test — they exercise the URL parser → gh fetch → template-rendering chain end-to-end.

## Implementation Plan

Collapsed from 5 steps to 2. The plan-phase work has done all the design; build is one file.

1. **Write the canonical command body.** This is the entire deliverable.
   - File: `rules/pr-feedback-judge.md` (new, regular file, no frontmatter — matches wiggum precedent)
   - Sections (in order):
     - Purpose / when-to-use.
     - **Load-bearing instruction**: "Fetch the actual comment text first, never judge from the URL alone" (Q3 finding F6).
     - URL shape table (lifted verbatim from Pinned Info, T1 paths shown).
     - Tier-detection block: T1 (`gh` + `gh auth status`) → T2 (loose `github` substring match against MCP server metadata) → fail loudly. Per-tier invocation recipes for at least one URL shape. **Advisory A2 (preflight v1):** explicitly anti-pattern "don't filesystem-scan for MCPs" — the detection signal is the harness's registered-MCP list (the same block exposed to the agent at invocation time), not a walk of `~/.cursor/projects/.../mcps/`.
     - The grounded intro from Q3 (verbatim).
     - The per-item block from Q3 (verbatim) and the conditional triage-table-when->5-items rule.
     - Orchestration walkthrough that includes the inlined batch-fetch instruction (B10): "if you end up with 3+ structurally-identical `gh api` calls, issue them as one batched pipeline, not a loop."
     - Failure-mode handling: malformed URL, T1 404, no-tier-available.
     - Example invocation against a public PR with one `#discussion_r…` and one whole-PR URL, showing the rendered output shape.
     - **Advisory A3 (preflight v2):** add a one-line tail tip: "to turn all `defer to follow-up` items into a GitHub issue, run `gh issue create --title 'Follow-ups from PR #N' --body-file <path>`" with a minimal suggested body template. Closes the loop on the most common post-verdict user action.
   - Creative refs: Q3 (final) → `creative-pr-feedback-judge-template-grounded.md`; Q2 → `creative-pr-feedback-judge-fetch-tiers.md`.

2. **Run inspection-grade validations B1 and B6–B10b** locally (pre-push); defer B2 to post-push. Manual smoke B11–B12 is QA-phase.

## Technology Validation

- **T1 — `gh` CLI 2.83.0**: installed locally, authenticated as `Texarkanine`, verified `gh api repos/Texarkanine/a16n/pulls/97/comments` returns clean JSON. Direct single-comment lookup `gh api repos/Texarkanine/a16n/pulls/comments/<id>` confirmed working — O(1), no list-and-filter needed.
- **T2 — GitHub MCP**: a GitHub MCP server (`user-github`, official-style implementation, 41 tools) was registered with the harness during plan-phase iteration. Inspected its tool surface: `pull_request_read` (method-dispatch with `get_review_comments` / `get_reviews` / `get_comments` / `get`), `issue_read` (method-dispatch with `get_comments`). **Confirmed: no single-comment-by-ID getter** — single-comment URLs require list-and-filter via the parent PR/issue. This validates the Q2 decision to demote MCP to T2 rather than T1.
- **MCP detection signal**: the agent's runtime context lists registered MCP servers with their names/identifiers/descriptions and tool schemas. Loose `github` substring match (case-insensitive) over server name/identifier/description is sufficient and operator-confirmed.
- **`ai-rizz` top-level command registration**: verified live during preflight v1 — `rules/*.md` files sync to `.cursor/commands/shared/<name>.md` and appear under "Available commands" in `ai-rizz list`. The `wiggum-niko-coderabbit-pr.md` precedent establishes this exact pattern.
- **Warehouse mining (Q3 plan-phase work)**: `cw-query` skill loaded; `query.py` resolved at `~/.cursor/plugins/local/cursor-warehouse/scripts/query.py`; prior CSVs from the warehouse-extract session reused at `/tmp/cursor-warehouse-pr-feedback-*.csv`. SQL extracted 21 URL-bearing user prompts; new artifact written at `/tmp/pr-feedback-user-prompts-extracted.csv`. Methodology fully documented in `creative-pr-feedback-judge-template-grounded.md`.

No new dependencies are introduced — `gh` and the GitHub MCP are deliberate user setup.

## Challenges & Mitigations

- **Challenge: ai-rizz reads from git remote, not local working tree.** End-to-end validation of B2 requires the branch to be pushed. → Mitigation: do B1 and B6–B10b locally without push; defer B2 to a single post-push check during QA.
- **Challenge: PR review fetch returns review bodies that may be empty** (review with no comment text but with inline comments attached). → Mitigation: command body specifies "skip review entries with empty body and no associated inline comments" in the orchestration walkthrough.
- **Challenge: `in_reply_to_id` chains** mean an inline comment can be a reply to an earlier comment, and judging it in isolation can miss context. → Mitigation: the fetch recipe for a single inline comment recommends a one-extra-call resolution of the parent thread (cheap, single call) before evaluation. Documented in the command body.
- **Challenge: Rate limiting / private repos.** → Mitigation: gh CLI handles auth and rate-limit errors with clear messages; the command body's failure-mode section instructs the agent to surface these verbatim rather than retry blindly.

## Status

- [x] Component analysis complete
- [x] Open questions resolved (Q1 superseded; Q2 final; Q3 final via warehouse mining; Q4 resolved during preflight — single-rule packaging)
- [x] Test planning complete (TDD-equivalent inspection plan; ruleset-specific B3/B4/B5 dropped)
- [x] Implementation plan complete (2 steps, both build-execution)
- [x] Technology validation complete
- [x] Preflight v1 (PASS; superseded by v2 after Q4 simplification)
- [x] Preflight v2 (PASS; A2 retained, A3 added; single-rule plan validated)
- [x] Build
- [x] QA (PASS — 1 trivial fix applied: inlined A3 minimal body template)
