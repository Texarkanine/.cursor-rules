# Task: PR Feedback Judge Command

* Task ID: pr-feedback-judge
* Complexity: Level 3
* Type: feature (new ruleset + command)

Build a Cursor command, packaged as the new `pr-feedback-judge` ruleset, that takes one or more GitHub PR-feedback URLs (whole PR, PR review, or single comment in any combination) and renders per-item "valid or invalid" verdicts using a formalized questioning/evaluation intro. The ruleset composes the existing `script-it-instead` rules so the batch-fetch guidance comes along automatically without duplicating content for consumers who already include them.

## Pinned Info

### URL Shape → GitHub API Endpoint

The command's dispatch logic depends entirely on classifying input URLs. This table is the contract. The API path is identical across the `gh` and anonymous-`curl` tiers (T1 and T2 — see Q2); the GitHub MCP tier (T0, when available) uses MCP tool names but operates on the same data shape.

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
- The command body itself depends at runtime on **at least one of**, in priority order: a registered GitHub MCP server (T0, harness-native, best), `gh` CLI authenticated (T1, dominant case), or `curl` for anonymous public-PR access (T2, best-effort). See Q2 for the tier chain. Always depends on the always-on `script-it-instead` rule that the same ruleset injects.

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

- [~] **Q1 — Questioning intro & per-item verdict template.** → **Provisionally resolved (v0)**: scaffolded intro (criteria: technical accuracy, scope alignment, severity) + hybrid verdict (triage table for all items, detail blocks for valid-only, summary tail). Templates drafted in `memory-bank/active/creative/creative-pr-feedback-judge-template.md`. **Subject to revision** in build phase Step 1 (warehouse mining) — the v0 template is grounded only in the warehouse summary I was handed, not in the actual user-prompt corpus. If mining surfaces patterns the v0 template misses or overfits, it is amended before the command body is written.
- [x] **Q2 — GitHub fetch tier strategy.** Reopened twice. Final resolution: **T0 (GitHub MCP, when registered with the harness) → T1 (`gh` CLI authenticated) → T2 (anonymous `curl`, best-effort, public PRs only)**. Tier order tracks user setup intent, not just tool availability. No env-var token harvesting. No per-tier sanity-check (long-list truncation is a "use a more specific URL" problem, not an engineering problem). All tiers reason over the same data shape (author / body / path / diff_hunk / verdict), so the parsing & template-rendering logic is tier-agnostic. See `memory-bank/active/creative/creative-pr-feedback-judge-fetch-tiers.md`.

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
- B8: The command body specifies the **tier-detection block in priority order T0→T1→T2** and shows one invocation example per tier for at least one URL shape, plus the API path table shared by T1/T2.
- B9: The command body includes the intro/verdict template (final, post-mining version) selected in Q1.
- B10: The command body explicitly references `script-it-instead` (so the agent knows to treat the fetch as a batch script, not a loop).
- B10a: The command body documents the private-repo failure mode for T2 (with the "install gh / register MCP" message) and the rate-limit failure mode for T2.

**Behavioral (manual smoke test)**

- B11: Pasting a real PR URL (e.g. `https://github.com/Texarkanine/a16n/pull/97`) plus a real `#discussion_r…` URL into a fresh chat with the command attached produces: one verdict per inline-review comment + one verdict per conversation comment + one verdict for the single inline comment, with no duplicate evaluations.
- B11a: Repeat B11 in a tier-degraded environment (`PATH` stripped of `gh`) — the command must still produce a correct rendering via T2 against a public PR.
- B11b: Repeat B11 against a known-private PR with no `gh` auth and no MCP — the command must surface the "install gh / register MCP" message rather than misclassifying or crashing.
- B12: An invalid / malformed URL produces a clear "could not classify" message, not a crash.

### Test Infrastructure

- **Framework**: none formally; this repo treats inspection + manual smoke as the test plane.
- **Test location**: N/A.
- **Conventions**: shell one-liners for B1–B5 and B7–B10; visual review for B6; live chat invocation for B11–B12.
- **New test files**: none. The validation procedure goes inline in the QA-phase commands.

### Integration Tests

- B11/B12 are the integration test — they exercise the URL parser → gh fetch → template-rendering chain end-to-end.

## Implementation Plan

Diagram-first. The new files are tiny and acyclic; the implementation order matches the dependency direction (leaves first). Build-phase steps 1 and 2 ground the template in real data before anything is written.

1. **Mine the warehouse for actual user questioning patterns.** The Q1 v0 template is grounded in the warehouse summary doc, not in the actual user-prompt corpus — operator flagged this as insufficient.
   - **Read fully**: `memory-bank/cursor_pull_request_feedback_references.md` (already in this task's context — re-read deliberately, do not skim).
   - **Run queries** against the local DuckDB warehouse using the `cw-query` skill (loaded via `/cw-query` in this conversation, or directly via `query.py`):
     - Pull the **first user message** for each of the ~40 sessions whose `text_content` contains a `github.com/.../pull/N` URL, with the system-context XML stripped (`regexp_extract` on `<user_query>…</user_query>`). This surfaces the actual phrasing the user uses to ask for feedback evaluation.
     - Pull the **specific message that contains the URL** when it isn't the first message — that's where the "evaluate this" framing usually sits. Same XML-stripping treatment.
     - Inspect the two CSVs the prior `/cw-query` session left at `/tmp/cursor-warehouse-pr-feedback-github-pull-urls.csv` and `/tmp/cursor-warehouse-pr-feedback-semantic-vs-url.csv` if they still exist on the build machine; regenerate via the same SQL (documented in the warehouse extract doc) if not.
     - Run a `cw-recall` semantic search for natural-language paraphrases of "judge this PR feedback" / "is this reviewer comment valid" / "evaluate each piece of feedback" to catch sessions the URL-only filter misses.
   - **Synthesize** what the user actually does in those threads: the recurring framing verbs ("evaluate", "judge", "weigh", "tell me if X is valid"), the recurring decision criteria they invoke explicitly, the recurring output structure they ask for (or accept without correction), and any consistent failure modes (e.g. agent emitting opinions before fetching, agent ignoring some comments).
   - **Compare to the v0 template** in `creative-pr-feedback-judge-template.md`. For each delta — wording, criteria, structure — decide: amend the template, or note explicitly why the v0 wins.
   - **Output**: a short addendum or revision to `creative-pr-feedback-judge-template.md` titled "Warehouse-mining update", documenting what was searched, what was found, and what (if anything) changed in the template. If nothing changes, that null result is itself documented with the queries that justified it. The (possibly amended) template at the end of this step is the **final** Q1 resolution.

2. **Write the canonical command body.** This is the bulk of the work.
   - Files: `rules/pr-feedback-judge.md` (new)
   - Sections (in order): purpose / when-to-use; URL shape table (lifted from Pinned Info, tier-agnostic API paths); **tier-detection block in priority order T0→T1→T2 + per-tier invocation recipes** (from Q2); the intro template (final, from Q1 + Step 1 mining); the per-item verdict format (final, from Q1 + Step 1 mining); orchestration walkthrough that ties batch-fetch (script-it-instead) to per-item evaluation; failure-mode handling — malformed URL, private-repo-without-auth, anonymous rate limit, no-tier-available; example invocation.
   - Creative refs: Q1 → `creative-pr-feedback-judge-template.md` (post-mining); Q2 → `creative-pr-feedback-judge-fetch-tiers.md`.

3. **Create the ruleset directory and symlinks.**
   - Files:
     - `rulesets/pr-feedback-judge/commands/pr-feedback-judge.md` → `../../../rules/pr-feedback-judge.md`
     - `rulesets/pr-feedback-judge/script-it-instead.mdc` → `../../rules/script-it-instead.mdc`
     - `rulesets/pr-feedback-judge/how-to-script-it-instead.mdc` → `../../rules/how-to-script-it-instead.mdc`
   - Verification: `find rulesets/pr-feedback-judge -type l -xtype l` is empty.

4. **Write the ruleset README.**
   - Files: `rulesets/pr-feedback-judge/README.md` (new)
   - Style: match `rulesets/shell/README.md` — brief purpose, links to each contained file, scope notes.
   - Content: explain the command's purpose, the four URL shapes accepted, the **tier-priority access model** (MCP preferred, gh fallback, anonymous best-effort for public PRs), and the rationale for bundling `script-it-instead`.

5. **Run inspection-grade validations B1–B10a.**
   - Mechanical shell one-liners; capture results into the QA report later.

6. **Manual smoke test B11/B11a/B11b/B12** (deferred to QA phase, but listed here so the implementer remembers it's part of "done").

## Technology Validation

- **T0 — GitHub MCP**: detection mechanism confirmed (the harness exposes registered MCP servers in the agent's context block; in this Cursor environment they live under `~/.cursor/projects/<proj>/mcps/<server>/tools/*.json`). No GitHub MCP is present in *this* build environment (current MCPs: `cursor-ide-browser`, `plugin-gitlab-GitLab`, `user-context7`), so T0 cannot be smoke-tested locally — but the command body design only requires the agent to *recognize* a github-flavored MCP tool when one is exposed; it does not bind to a specific server.
- **T1 — `gh` CLI 2.83.0**: installed locally, authenticated as `Texarkanine`, verified `gh api repos/Texarkanine/a16n/pulls/97/comments` returns clean JSON.
- **T2 — anonymous REST**: `curl -fsS https://api.github.com/repos/Texarkanine/a16n/pulls/comments/3177417607` confirmed during plan to return identical JSON shape to T1, including `diff_hunk` and `pull_request_review_id`. Anonymous rate limit confirmed at `x-ratelimit-limit: 60` per hour; that's plenty for a single PR review and we are explicitly not engineering around it.
- **`jq` 1.6**: installed locally; treated as opportunistic in T2 (T2 falls back to a `python3 -c '…'` stdlib parse if absent).
- **`ai-rizz`**: installed at `/home/mobaxterm/.local/bin/ai-rizz`; `ai-rizz list` works and already lists the existing `script-it` ruleset and `wiggum-niko-coderabbit-pr` command, confirming the conventions we're modeling on.
- **Warehouse access for build Step 1**: the `cw-query` and `cw-recall` skills are loaded in this conversation; `query.py` and `vsearch.py` are resolvable per their respective SKILL files. No new install required.

No new dependencies are introduced — every tool in the tier chain is either deliberate user setup (T0/T1) or already present in the audience's environment (T2's `curl`).

## Challenges & Mitigations

- **Challenge: ai-rizz reads from git remote, not local working tree.** End-to-end validation of B2/B3 requires the branch to be pushed. → Mitigation: do B1, B4, B5, B7–B10 locally without push; defer B2/B3 to a single post-push check during QA. Document this expectation in the QA section.
- **Challenge: PR review fetch returns review bodies that may be empty** (review with no comment text but with inline comments attached). → Mitigation: command body must specify "skip review entries with empty body and no associated inline comments" in the orchestration walkthrough; covered by Q1 template design.
- **Challenge: `in_reply_to_id` chains** mean an inline comment can be a reply to an earlier comment, and judging it in isolation can miss context. → Mitigation: the fetch recipe for a single inline comment recommends a one-extra-call resolution of the parent thread (cheap, single call) before evaluation. Documented in the command body.
- **Challenge: Rate limiting / private repos.** → Mitigation: gh CLI handles auth and rate-limit errors with clear messages; the command body's failure-mode section instructs the agent to surface these verbatim rather than retry blindly.

## Status

- [x] Component analysis complete
- [x] Open questions resolved (Q1 v0 + Q2 final; Q1 final pending build Step 1 mining as designed)
- [x] Test planning complete (TDD-equivalent inspection plan)
- [x] Implementation plan complete (build Step 1 = warehouse mining; Step 2+ = build proper)
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
