---
task_id: pr-feedback-judge
complexity_level: 3
date: 2026-05-03
status: completed
---

# TASK ARCHIVE: PR Feedback Judge Command

## SUMMARY

Delivered `/pr-feedback-judge` as a single canonical Cursor slash command at `rules/pr-feedback-judge.md`. The command accepts any mix of GitHub PR-feedback URLs (whole PR, a specific PR review, inline `#discussion_r…`, or `#issuecomment-…`), fetches comment bodies and context via **T1** authenticated `gh` CLI (preferred) or **T2** a harness-registered GitHub MCP server (loose-detected by `github` substring in server metadata), and renders per-item verdicts using a **corpus-grounded** rubric: separate answers for **Valid?**, **Worth fixing?**, **In scope for this PR?**, plus an explicit disposition (`fix in this PR` / `defer to follow-up` / `dismiss with acknowledgment` / `dismiss`). Anonymous access was explicitly cut; neither tier available yields one actionable error message.

Packaging collapsed during preflight from a ruleset plus always-on `script-it-instead` to a **single top-level rule file**: corpus evidence showed typical asks are 1–3 items, so batch-fetch discipline is **inlined** in the command body (3+ structurally identical `gh api` calls → one batched pipeline) rather than bundling a separate rule.

Post-reflect rework removed YAGNI sections (e.g. “When to use”, T2 access-pattern table, filesystem-scan-for-MCPs advisory text), softened the fetch-first wording so reviewer text is mandatory input but not the only evidence, and re-passed QA.

## REQUIREMENTS

- **Inputs:** Whole PR URL; `#pullrequestreview-<id>`; `#discussion_r<id>`; `#issuecomment-<id>` — classify and dispatch without crashing on malformed URLs.
- **Behavior:** Apply grounded intro and per-item template (Q3); conditional triage table only when **>5** items; load-bearing **fetch first** instruction; inlined batch-fetch when many identical `gh api` shapes; failure modes for 404 and no-tier.
- **Packaging:** Canonical source only at `rules/pr-feedback-judge.md` (ai-rizz / a16n sync downstream). No ruleset wrapper.
- **Out of scope:** `/nk-chat` memory coupling (separate issue); verdict persistence; env-var token harvesting; anonymous GitHub access.

## IMPLEMENTATION

- **Primary artifact:** `rules/pr-feedback-judge.md` (~158 lines post-rework) — sections: purpose + access requirements → load-bearing fetch-first H2 → URL→endpoint table → tier detection (T1→T2→fail) with `gh api` recipes → grounded intro and per-item format (verbatim from Q3) → conditional triage → tail with `gh issue create` follow-up tip and minimal body template → orchestration + batch-fetch instruction → failure modes → example invocation (`Texarkanine/a16n#97`).
- **Design lineage:** Plan iterated through multiple Q2 revisions (anonymous tiers dropped), Q3 promoted from build sub-step to dedicated creative (warehouse mining of 21 URL-bearing user prompts → 12 clean signals), Q4 collapsed ruleset to single file after preflight v2 traced Q3’s “1–3 items per ask” into packaging.
- **Post-reflect edits:** Dropped “When to use”; softened exclusivity of “only evidence” to “MUST be retrieved and considered”; removed MCP filesystem-scan anti-pattern prose, “popular MCPs” scaffolding sentence, and T2 table — agent relies on URL table + runtime MCP schemas.

### Creative phase — Q2 fetch tiers (inlined summary)

**Decision:** Ordered chain **T1 (`gh` authenticated) → T2 (GitHub MCP, loose `github` match) → fail loudly.**

**Rationale:** `gh` gives O(1) REST paths for single-comment anchors; typical MCP tool surfaces are PR/issue-scoped method dispatch (list-and-filter for single comments). Anonymous REST and HTML scrape tiers removed per operator.

**T1 detection:** `command -v gh && gh auth status`. **T2 detection:** any registered MCP server whose name/identifier/description contains `github` (case-insensitive); agent reads tool schemas at runtime.

**URL→T1 `gh api` paths (representative):**

| Fragment | T1 paths (under `api.github.com`) |
|----------|-----------------------------------|
| (none) whole PR | `pulls/{N}/comments`, `issues/{N}/comments`, `pulls/{N}/reviews` (paginated) |
| `#pullrequestreview-{rid}` | `pulls/{N}/reviews/{rid}`, `pulls/{N}/reviews/{rid}/comments` |
| `#discussion_r{cid}` | `pulls/comments/{cid}` |
| `#issuecomment-{cid}` | `issues/comments/{cid}` |

**Failure messages:** T1 404 → private/deleted/malformed guidance; no tier → install `gh` + `gh auth login`, or register a GitHub MCP.

### Creative phase — Q3 grounded template (inlined summary)

**Method:** SQL extraction via cursor-warehouse (`cw-query`) of user-side URL-bearing messages; 21 extracted, 12 clean “evaluate this feedback” signals.

**Findings F1–F6 (condensed):**

- **F1:** User vocabulary is **valid / worth fixing / in scope for this PR** — not generic “technical accuracy / severity / scope.”
- **F2:** User wants **three separate** criterion answers with “why,” often as a numbered list.
- **F3:** Answers compose into a **Disposition** line (four fixed values).
- **F4:** Real ask sizes **1–3 items** (median 2); triage table only when **>5** items.
- **F5:** Terse opener (“PR feedback:”) and insistence on **why**.
- **F6:** Corpus-attested failure: agent judged **without** fetching the linked comment → **fetch first** is load-bearing.

**Shipped template:** Intro (criteria + disposition composition) + per-item block with **Where**, **Reviewer’s point**, three criterion lines with ✅/❌/🕒, **Disposition** — plus optional triage table when >5 items, and a count tail.

### Creative phase — Q1 v0 (superseded)

v0 (`creative-pr-feedback-judge-template.md`) chose I-Scaffolded + V-Hybrid with “technical accuracy / scope / severity” and default triage table. **Superseded** by Q3 after operator required corpus grounding; v0 retained in archive narrative only for audit trail.

## TESTING

No automated test framework in this repo. Validation was **inspection-grade** (B1, B6–B10b) plus QA semantic review; behavioral smokes B11–B12 and post-push **B2** (`ai-rizz list` shows `/pr-feedback-judge`) called out in plan as manual / post-push where applicable.

**Executed:** B1 (regular file), B7 (four URL shapes), B8 (tier order + `gh` paths + T2 via schema reading — post-rework without separate T2 table), B9 (grounded intro + per-item + conditional triage), B10 (batch 3+ identical `gh api`), B10a/B10b (failure messages + fetch-first section). QA PASS; trivial fix: inlined minimal markdown body template under A3 tip. Post-reflect rework re-checked fences, tier order, B7/B10a/B10b.

## LESSONS LEARNED

- **Corpus mining beats intuition** for prompt design: real user vocabulary (“valid / worth fixing / in scope”) replaced analyst paraphrases only after reading actual prompts.
- **Preflight traces creative implications into packaging:** Q3’s small batch sizes enabled Q4 — dropping ruleset and always-on `script-it-instead`.
- **Iteration that consistently deletes scope is healthy:** multiple Q2 reopenings removed anonymous tiers, env groveling, and ruleset complexity.
- **QA “Completeness” catches plan hand-waves:** A3 asked for a “template”; natural-language description was insufficient — concrete template fixed in one edit.
- **Self-documenting “When to use” in command bodies is a category error** for manual-only Cursor commands; invocation choice happens before the body loads.
- **Preflight advisories need cited failure modes** or they risk YAGNI (e.g. filesystem-scan-for-MCPs never observed live).
- **Operator questions vs action items:** messages with `?` should be answered explicitly before treating them as build tasks.

## PROCESS IMPROVEMENTS

- When an advisory requires an artifact (“provide a template”), put the artifact or exact stub in the advisory text.
- Run **packaging implication checks** after creative: “Given evidence X, does the plan still need dependency Y?”
- For documentation-heavy deliverables, **operator presence at QA** improves YAGNI passes (“would I read this as the agent?”).
- **Reflect-as-terminal-with-feedback:** Post-reflect reviewer-style feedback can be handled as a rework cycle without rewinding the whole phase machine if QA criteria still pass after edits.

## TECHNICAL IMPROVEMENTS

- If the “no When-to-use in command bodies” pattern repeats across commands, consider promoting it to `memory-bank/systemPatterns.md`.
- Optional: after push, confirm **B2** registration via `ai-rizz list` in environments that read remote rules.

## NEXT STEPS

None required for task closure. Optional verification: run **B2** / live **B11–B12** smokes after installing from remote if not already done.

---

## APPENDIX A — Full reflection document (inlined)

The following was the task reflection prior to archive consolidation (including post-reflect addendum).

---

task_id: pr-feedback-judge  
date: 2026-05-03  
complexity_level: 3  

### Reflection: PR Feedback Judge Command — Summary

Shipped `rules/pr-feedback-judge.md` with corpus-grounded rubric and T1→T2→fail fetch strategy. Build was transcription-heavy; QA caught missing A3 template body; post-reflect rework applied four YAGNI/wording fixes.

### Requirements vs Outcome

All planned requirements delivered; out-of-scope items respected.

### Plan Accuracy

Two-step build matched work shape. Plan mildly under-specified A3 template literal — QA fixed.

### Creative Phase Review

Q1 v0 superseded; Q2 tiers held; Q3 verbatim in command; F6 fetch-first earned prominent placement.

### Build & QA Observations

Single trivial QA fix; no FAIL→Plan cycle.

### Cross-Phase Analysis

Chain: Q3 F4 (small batch sizes) → preflight v2 Q4 (single file). A2 advisory influenced early drafts; later rework dropped A2 text as YAGNI.

### Insights (technical)

- Corpus mining > intuition for prompts.
- Top-level `rules/*.md` fits “one command, no composition.”

### Insights (process)

- Preflight catches design-implication misses.
- Trivial QA fixes cheap vs slow live loops.
- Many plan iterations that reduce complexity are net positive.

### Addendum — Post-Reflect Rework (2026-05-03)

1. Dropped “When to use.”  
2. Softened load-bearing “only evidence” wording.  
3. Dropped filesystem-scan-for-MCPs anti-pattern (YAGNI).  
4. Dropped “popular MCPs / no single-comment getter” sentence.  
5. Dropped T2 access-pattern table (YAGNI).  

Cross-cycle: command invocation criteria belong outside body; preflight advisories need evidence; operator QA improves YAGNI; surface operator questions before acting.

---

## APPENDIX B — Creative: grounded template (verbatim decision blocks)

**Intro (always emitted):**

> Evaluating each piece of PR feedback. I'll fetch the actual comment text first — never judging from the URL alone — then for each item answer three questions and state the disposition.
>
> 1. **Valid?** Is the reviewer technically right about the code? Why or why not?
> 2. **Worth fixing?** Is the issue real and severe enough to act on at all? Why or why not?
> 3. **In scope for this PR?** Should it be fixed on this branch, deferred to a follow-up, or dismissed? Why or why not?
>
> The three answers compose into a disposition. Feedback can be valid but not worth fixing, or valid and worth fixing but out of scope for *this* PR — I'll spell each one out.

**Per-item block structure:** `### Item N — [link](url) by @author`, **Where**, **Reviewer’s point**, three criterion lines, **Disposition** with four allowed values.

**Triage table:** only when item count > 5.

**Tail:** counts of items / fix now / deferred / dismissed.

*(Implementation note: post-reflect command body softens “never judging from the URL alone” pairing with “MUST be retrieved and considered” rather than “only evidence.”)*

---

## APPENDIX C — Progress history summary (inlined)

Ephemeral `progress.md` chronicled: Niko init → L3 → plan v1–v4 → creative Q1/Q3 → preflight v1 (PASS, advisories) → plan amendment Q4 + preflight v2 (PASS, single-file plan) → BUILD → QA → REFLECT → post-reflect REWORK (YAGNI cuts, QA re-pass). Key milestone: **Preflight v2** explicitly connected Q3 corpus batch-size evidence to dropping the ruleset and `script-it-instead` bundling.
