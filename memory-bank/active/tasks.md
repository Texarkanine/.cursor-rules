# Task: PR Feedback Judge Command

* Task ID: pr-feedback-judge
* Complexity: Level 3
* Type: feature (new ruleset + command)

Build a Cursor command, packaged as the new `pr-feedback-judge` ruleset, that takes one or more GitHub PR-feedback URLs (whole PR, PR review, or single comment in any combination) and renders per-item "valid or invalid" verdicts using a formalized questioning/evaluation intro. The ruleset composes the existing `script-it-instead` rules so the batch-fetch guidance comes along automatically without duplicating content for consumers who already include them.

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

- **`rules/pr-feedback-judge.md`** (NEW): canonical command body. Lives top-level in `rules/` matching the `wiggum-niko-coderabbit-pr.md` convention. Contains: the questioning/evaluation intro template (TBD by creative), URL-classification rubric (above), the gh-CLI fetch recipe, the per-item verdict format, and the orchestration prose that tells the agent how to chain them.
- **`rulesets/pr-feedback-judge/`** (NEW directory): ruleset bundle. Contents:
  - `commands/pr-feedback-judge.md` → symlink to `../../../rules/pr-feedback-judge.md`
  - `script-it-instead.mdc` → symlink to `../../rules/script-it-instead.mdc`
  - `how-to-script-it-instead.mdc` → symlink to `../../rules/how-to-script-it-instead.mdc`
  - `README.md` (NEW): standard ruleset README in the style of `rulesets/shell/README.md`.

### Cross-Module Dependencies

- `rulesets/pr-feedback-judge/` → `rules/pr-feedback-judge.md`, `rules/script-it-instead.mdc`, `rules/how-to-script-it-instead.mdc` (all via symlink)
- The command body itself depends at runtime on **at least one of**, in priority order: `gh` CLI authenticated (T1, preferred — direct single-comment lookups, batches with `script-it-instead`), or a registered GitHub MCP server (T2, fallback — harness-native but list-and-filter for single-comment URLs). Anonymous access is cut entirely. See Q2 for the tier chain. Always depends on the always-on `script-it-instead` rule that the same ruleset injects.

### Boundary Changes

- **New public surface**: `/pr-feedback-judge <url>...` slash command becomes available to anyone who installs the ruleset via `ai-rizz add ruleset pr-feedback-judge`.
- No existing ruleset, rule, or skill changes shape. `script-it-instead` and `how-to-script-it-instead` are referenced (via symlink), not modified.

### Invariants & Constraints

1. **Canonical-source rule**: the command body MUST be edited only at `rules/pr-feedback-judge.md` (per `agent-customization-locations.mdc`). Any `.cursor/` or `.claude/` copies are downstream of `ai-rizz` / `a16n` sync.
2. **Composition without duplication**: `script-it-instead.mdc` and `how-to-script-it-instead.mdc` MUST be referenced via symlink, not copied. ai-rizz dedupes by file path, so a user who has both `script-it` and `pr-feedback-judge` rulesets installed sees each rule exactly once.
3. **No runtime persistence**: the command renders verdicts to chat and does not write to the memory bank. (Persistence concerns are explicitly out of scope per the brief.)
4. **No Niko coupling**: the command MUST work both inside and outside a live Niko conversation. Memory-bank-context loading is `/nk-chat`'s job (issue #63, separate thread).
5. **Batch-fetch discipline**: per `script-it-instead`, N input URLs MUST NOT produce N+ tool calls for the fetch step — pagination per URL is unavoidable, but per-comment lookups must be batched.

## Open Questions

- [x] **Q1 — Questioning intro & per-item verdict template (v0).** Provisionally resolved during plan-phase creative as scaffolded intro + hybrid (triage-table + valid-detail) verdict. Operator flagged the grounding (a summary doc only, not the actual user-prompt corpus) as insufficient. v0 is preserved in `creative-pr-feedback-judge-template.md` for design-history reasons but is **superseded by Q3** (see below). The v0 doc has a banner pointing at the grounded version.
- [x] **Q2 — GitHub fetch tier strategy.** Reopened three times. Final resolution: **T1 (`gh` CLI authenticated, preferred — direct single-comment lookups, batches with `script-it-instead`) → T2 (GitHub MCP, loose-detected by case-insensitive `github` substring match against MCP server name/identifier/description; agent reads tool schemas at runtime) → fail loudly**. Anonymous access cut. No env-var token harvesting. No sanity-check. Verified the popular `user-github` MCP exposes only PR/issue-scoped method-dispatch tools (no single-comment-by-ID getter), which is why T1 wins on efficiency. See `memory-bank/active/creative/creative-pr-feedback-judge-fetch-tiers.md`.
- [x] **Q3 — Questioning intro & per-item verdict template (grounded).** Promoted from a build step to its own creative exploration per operator: this is the real meat of the prompt design. Mined the actual user-prompt corpus from the local Cursor warehouse (21 URL-bearing user messages extracted, 12 clean signal). Findings: the user's actual criteria vocabulary is **valid / worth fixing / in scope for this PR** (not "technical accuracy / severity / scope alignment"); the user wants the three questions answered separately, not collapsed; the user wants an explicit disposition (fix-now / defer-follow-up / dismiss) which is the composition of the three answers; real ask sizes are 1–3 items (not 30) so the triage table demotes to >5-items-only; corpus shows a corpus-attested failure mode (agent answered before fetching the linked comment) that requires a load-bearing "fetch first" instruction in the intro. Final template in `memory-bank/active/creative/creative-pr-feedback-judge-template-grounded.md`.

(URL parsing/dispatch was flagged as open in the projectbrief but collapsed: regex on the URL fragment, mapping unambiguous and now in the Pinned Info table.)

## Test Plan (TDD)

### Behaviors to Verify

This is a documentation/rule repo with no automated test framework (confirmed: no `tests/`, `test/`, `package.json`, or `Makefile`). "Tests" are inspection-grade validations. Each behavior maps to one mechanical check.

**Packaging**

- B1: `rulesets/pr-feedback-judge/` exists and is a directory.
- B2: `ai-rizz list` shows `pr-feedback-judge` under "Available rulesets" (after push to remote — ai-rizz reads remote per `techContext.md`).
- B3: `ai-rizz list` shows `/pr-feedback-judge` under "Available commands".
- B4: All symlinks in the ruleset resolve (`find rulesets/pr-feedback-judge -type l -xtype l` returns empty).
- B5: The ruleset includes README.md, `commands/pr-feedback-judge.md`, `script-it-instead.mdc`, and `how-to-script-it-instead.mdc` — and nothing else.

**Command-body well-formedness**

- B6: `rules/pr-feedback-judge.md` parses as Markdown without lint errors (using whatever markdown linter the repo uses; if none, manual visual review).
- B7: The command body documents all four URL shapes from the Pinned Info table.
- B8: The command body specifies the **tier-detection block in priority order T1 (`gh`) → T2 (GitHub MCP, loose-detected) → fail** and shows the `gh api` invocations for each URL shape; for T2, describes the access pattern (which logical operation per URL shape) without hardcoding MCP tool names.
- B9: The command body includes the grounded intro and per-item block from Q3 verbatim (intro + per-item block always; triage table conditional on >5 items).
- B10: The command body explicitly references `script-it-instead` (so the agent knows to treat the fetch as a batch script, not a loop).
- B10a: The command body documents the failure modes from Q2: 404 in T1 → "private or deleted or malformed"; no tier available → "install gh and run gh auth login, or register a GitHub MCP server."
- B10b: The command body includes the load-bearing "fetch first, never judge from the URL alone" instruction from Q3 finding F6.

**Behavioral (manual smoke test)**

- B11: Pasting a real PR URL (e.g. `https://github.com/Texarkanine/a16n/pull/97`) plus a real `#discussion_r…` URL into a fresh chat with the command attached produces: one verdict per inline-review comment + one verdict per conversation comment + one verdict for the single inline comment, with no duplicate evaluations.
- B11a: Repeat B11 in a tier-degraded environment (`PATH` stripped of `gh`) — the command must still produce a correct rendering via T2 (GitHub MCP).
- B11b: Repeat B11 with neither `gh` nor a registered GitHub MCP — the command must surface the "install gh / register MCP" message rather than misclassifying or crashing or trying to fetch anonymously.
- B12: An invalid / malformed URL produces a clear "could not classify" message, not a crash.

### Test Infrastructure

- **Framework**: none formally; this repo treats inspection + manual smoke as the test plane.
- **Test location**: N/A.
- **Conventions**: shell one-liners for B1–B5 and B7–B10; visual review for B6; live chat invocation for B11–B12.
- **New test files**: none. The validation procedure goes inline in the QA-phase commands.

### Integration Tests

- B11/B12 are the integration test — they exercise the URL parser → gh fetch → template-rendering chain end-to-end.

## Implementation Plan

The plan-phase work has done all the design. Build phase is straight execution — write the file, lay down the symlinks, write the README, validate.

1. **Write the canonical command body.** This is the bulk of the work.
   - Files: `rules/pr-feedback-judge.md` (new)
   - Sections (in order):
     - Purpose / when-to-use.
     - **Load-bearing instruction**: "Fetch the actual comment text first, never judge from the URL alone" (Q3 finding F6).
     - URL shape table (lifted verbatim from Pinned Info, T1 paths shown).
     - Tier-detection block: T1 (`gh` + `gh auth status`) → T2 (loose `github` substring match against MCP server metadata) → fail loudly. Per-tier invocation recipes for at least one URL shape.
     - The grounded intro from Q3 (verbatim).
     - The per-item block from Q3 (verbatim) and the conditional triage-table-when->5-items rule.
     - Orchestration walkthrough that ties batch-fetch (script-it-instead) to per-item evaluation.
     - Failure-mode handling: malformed URL, T1 404, no-tier-available.
     - Example invocation against a public PR with one `#discussion_r…` and one whole-PR URL, showing the rendered output shape.
   - Creative refs: Q3 (final) → `creative-pr-feedback-judge-template-grounded.md`; Q2 → `creative-pr-feedback-judge-fetch-tiers.md`.

2. **Create the ruleset directory and symlinks.**
   - Files:
     - `rulesets/pr-feedback-judge/commands/pr-feedback-judge.md` → `../../../rules/pr-feedback-judge.md`
     - `rulesets/pr-feedback-judge/script-it-instead.mdc` → `../../rules/script-it-instead.mdc`
     - `rulesets/pr-feedback-judge/how-to-script-it-instead.mdc` → `../../rules/how-to-script-it-instead.mdc`
   - Verification: `find rulesets/pr-feedback-judge -type l -xtype l` is empty.

3. **Write the ruleset README.**
   - Files: `rulesets/pr-feedback-judge/README.md` (new)
   - Style: match `rulesets/shell/README.md`.
   - Content: command purpose, four URL shapes accepted, tier-priority access model (`gh` preferred, GitHub MCP fallback, anonymous not supported), rationale for bundling `script-it-instead`.

4. **Run inspection-grade validations B1–B10b.** Mechanical shell one-liners; capture results for the QA report.

5. **Manual smoke test B11/B11a/B11b/B12** (QA phase, but listed here so it's not forgotten as part of "done").

## Technology Validation

- **T1 — `gh` CLI 2.83.0**: installed locally, authenticated as `Texarkanine`, verified `gh api repos/Texarkanine/a16n/pulls/97/comments` returns clean JSON. Direct single-comment lookup `gh api repos/Texarkanine/a16n/pulls/comments/<id>` confirmed working — O(1), no list-and-filter needed.
- **T2 — GitHub MCP**: a GitHub MCP server (`user-github`, official-style implementation, 41 tools) was registered with the harness during plan-phase iteration. Inspected its tool surface: `pull_request_read` (method-dispatch with `get_review_comments` / `get_reviews` / `get_comments` / `get`), `issue_read` (method-dispatch with `get_comments`). **Confirmed: no single-comment-by-ID getter** — single-comment URLs require list-and-filter via the parent PR/issue. This validates the Q2 decision to demote MCP to T2 rather than T1.
- **MCP detection signal**: the directory layout `~/.cursor/projects/<proj>/mcps/<server>/SERVER_METADATA.json` exposes the server's name and identifier; the agent's runtime context also lists registered MCP servers and their tool schemas. Loose `github` substring match (case-insensitive) over server name/identifier/description is sufficient and operator-confirmed.
- **`ai-rizz`**: installed at `/home/mobaxterm/.local/bin/ai-rizz`; `ai-rizz list` works and already lists the existing `script-it` ruleset and `wiggum-niko-coderabbit-pr` command, confirming the conventions we're modeling on.
- **Warehouse mining (Q3 plan-phase work)**: `cw-query` skill loaded; `query.py` resolved at `~/.cursor/plugins/local/cursor-warehouse/scripts/query.py`; prior CSVs from the warehouse-extract session reused at `/tmp/cursor-warehouse-pr-feedback-*.csv`. SQL extracted 21 URL-bearing user prompts; new artifact written at `/tmp/pr-feedback-user-prompts-extracted.csv`. Methodology fully documented in `creative-pr-feedback-judge-template-grounded.md`.

No new dependencies are introduced — `gh` and the GitHub MCP are deliberate user setup.

## Challenges & Mitigations

- **Challenge: ai-rizz reads from git remote, not local working tree.** End-to-end validation of B2/B3 requires the branch to be pushed. → Mitigation: do B1, B4, B5, B7–B10 locally without push; defer B2/B3 to a single post-push check during QA. Document this expectation in the QA section.
- **Challenge: PR review fetch returns review bodies that may be empty** (review with no comment text but with inline comments attached). → Mitigation: command body must specify "skip review entries with empty body and no associated inline comments" in the orchestration walkthrough; covered by Q1 template design.
- **Challenge: `in_reply_to_id` chains** mean an inline comment can be a reply to an earlier comment, and judging it in isolation can miss context. → Mitigation: the fetch recipe for a single inline comment recommends a one-extra-call resolution of the parent thread (cheap, single call) before evaluation. Documented in the command body.
- **Challenge: Rate limiting / private repos.** → Mitigation: gh CLI handles auth and rate-limit errors with clear messages; the command body's failure-mode section instructs the agent to surface these verbatim rather than retry blindly.

## Status

- [x] Component analysis complete
- [x] Open questions resolved (Q1 superseded; Q2 final; Q3 final via warehouse mining)
- [x] Test planning complete (TDD-equivalent inspection plan)
- [x] Implementation plan complete (5 steps, all build-execution; design fully done in plan)
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
