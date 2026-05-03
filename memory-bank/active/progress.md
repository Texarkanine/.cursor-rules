# Progress: PR Feedback Judge Command

**Complexity:** Level 3

## Summary

Build a new Cursor ruleset (`pr-feedback-judge`) that exposes a slash command for evaluating GitHub PR review feedback. The command accepts any mix of whole-PR, PR-review, and single-comment URLs; batch-fetches the relevant GitHub data via `gh` CLI (preferred) or a registered GitHub MCP server (fallback) — anonymous access cut entirely; and renders per-item dispositions ("fix in this PR" / "defer to follow-up" / "dismiss") by answering the user's three actual recurring criteria — **valid?**, **worth fixing?**, **in scope for this PR?** — with a corpus-grounded template mined from 21 real user prompts. Ships as a ruleset that composes `script-it-instead` (via symlinks). Out of scope: `/nk-chat` (issue #63), verdict persistence, env-var token harvesting, anonymous fallback.

## History

- **Niko init / intent clarification — complete.**
- **Complexity analysis — complete.** Level 3.
- **Plan v1 — research.** Two of three projectbrief open questions collapsed; one remained (Q1 template wording). *Defect: prematurely closed Q2 by overfitting to local `gh`.*
- **Creative — Q1 v0.** Scaffolded intro + hybrid verdict (later superseded).
- **Plan v2 — Q2 reopened, first time.** Operator: drive-by reviews must work too. Resolved as T1 gh → T2/T3 anon-curl → T5 web-fetch with significant anon engineering.
- **Plan v3 — Q2 reopened, second time + Q1 grounding required.** Operator: anon is third-class, no env-var grovel, no sanity check. Add warehouse mining as a build step.
- **Plan v4 (current) — Q2 reopened, third time + Q3 promoted.** Operator added a real GitHub MCP to the harness. Inspection of `user-github` confirmed it has no single-comment-by-ID getter (PR/issue-scoped method-dispatch only). That flips the tier order: T1 `gh` is now preferred (direct lookups + native `script-it-instead` batching); T2 GitHub MCP is fallback (loose-detected by `github` substring match against server metadata). Anonymous access cut. Operator also promoted warehouse-mining from a build step to its own creative exploration (Q3) — "the real meat of the prompt design."
- **Creative — Q3 (warehouse-grounded template).** Mined 21 URL-bearing user prompts from the local Cursor warehouse, filtered to 12 clean signals. Findings: user's actual criteria vocabulary is **valid / worth fixing / in scope for this PR**; user wants three separate answers per item; user wants explicit disposition (4 values); real ask sizes are 1–3 items so triage table demotes to >5-items-only; corpus shows a load-bearing failure mode where the agent answered before fetching the linked comment. Final template in `creative-pr-feedback-judge-template-grounded.md`. v0 marked superseded.
- **Plan — finalized v4.** All open questions resolved. Implementation plan reduced to 5 build-execution steps (warehouse mining is plan-phase work, done).

## 2026-05-03 - PREFLIGHT - PASS

* Work completed
    - Verified convention compliance: top-level `rules/pr-feedback-judge.md` matches wiggum precedent; ruleset symlink composition matches `rulesets/script-it/` exactly; README style matches `rulesets/shell/README.md`.
    - **Live-verified** the novel `commands/` subdirectory sub-convention by scaffolding a throwaway test ruleset, running `ai-rizz sync`, and confirming `.md` in `rulesets/*/commands/` lands at `.cursor/commands/shared/` while `.mdc` symlinks land at `.cursor/rules/shared/`. Dedup across co-installed rulesets confirmed.
    - Validated all B1–B12 map to concrete plan steps; no missing implementation paths.
    - Confirmed no conflicts with existing rules/rulesets/skills.
* Decisions made
    - PASS with 2 advisories folded into the plan:
        - **A1**: README should document rule-vs-ruleset install paths (`ai-rizz add rule` for command-only, `ai-rizz add ruleset` for bundled composition).
        - **A2**: Command body's T2 detection block should explicitly anti-pattern filesystem-scanning for MCPs — detection is from the harness's registered-MCP list.
* Insights
    - Top-level `rules/*.md` files auto-register as slash commands in ai-rizz (synced to `.cursor/commands/shared/`), independent of any ruleset membership. This is the precedent-established mechanism (wiggum). The ruleset's role is purely composition — bundling support rules and providing a single install entry point.
    - ai-rizz's flattening of ruleset members into type-specific sync directories (`.mdc` → rules/, `.md` → commands/) means the `commands/` subdir inside a ruleset is an organizational convenience in source, not a structural requirement in the sync target.

## 2026-05-03 - PLAN AMENDMENT Q4 + PREFLIGHT v2 - PASS

* Work completed
    - Operator challenged the ruleset-plus-`script-it-instead` packaging: "if the mechanics of the judge command aren't even likely to proc `script-it-instead`, maybe we're just writing a single command in `rules/*.md`."
    - Mapped the command's fetch mechanics against `script-it-instead`'s "third structurally-similar call" threshold. Only invocation shape that trips it: 3+ single-comment URLs of the same anchor type. Corpus evidence (Q3): real ask sizes are 1–3 items, median 2, mode 1 — the batch case is a minority scenario.
    - **Q4 resolved: drop the ruleset.** Collapse deliverable to a single `rules/pr-feedback-judge.md` top-level command. Inline targeted batch-fetch guidance into the command body's orchestration walkthrough (targeted to the fetch step, not always-on across all conversations).
    - Amended `tasks.md`: rewrote Component Analysis, Invariants, Test Plan (dropped B3/B4/B5 as ruleset-specific), Implementation Plan (collapsed from 5 steps to 2), and Challenges.
    - Amended `projectbrief.md` Packaging section to match.
    - Surgical note added to `creative-pr-feedback-judge-fetch-tiers.md` "README implications" section → now "Command-body preamble implications."
    - Re-ran preflight against the simplified plan.
* Decisions made
    - **Q4 final**: single top-level `rules/pr-feedback-judge.md`. No ruleset. No symlinks. No `script-it-instead` always-on dependency. Batch-fetch discipline inlined where it's actually relevant (the fetch step).
    - **Preflight v2**: PASS. 1 advisory (A3 — optional follow-up-issue tip in the tail). A2 from v1 retained. A1 from v1 dropped (no longer applicable). No novel conventions introduced; the plan now hews exactly to the wiggum precedent.
* Insights
    - "Compose an always-on rule" and "inline the one instruction that actually matters" are different tradeoffs. Always-on is the right call when the rule's guidance applies broadly across many agent actions; inlining is the right call when the guidance is specific to one step of one command. The plan's original instinct to bundle `script-it-instead` was right pattern-matching but wrong fit — the command's fetch is too bounded for an always-on rule to earn its keep.
    - Preflight caught a thing creative didn't (and shouldn't have): the *packaging* consequence of the Q3 corpus evidence. Q3 said "real ask sizes are 1–3 items." Nobody followed the implication into "so the batch-fetch rule doesn't trigger, so why are we bundling it?" until operator asked directly. Worth remembering: creative answers the design question it's scoped to; preflight's job is to notice when a design answer renders a plan decision moot.

## 2026-05-03 - BUILD - COMPLETE

* Work completed
    - Wrote `rules/pr-feedback-judge.md` (single-file deliverable, 10.5KB) per the plan's section order: purpose + access requirements → load-bearing fetch-first instruction → URL-shape→endpoint table → tier-detection block (T1 gh → T2 GitHub MCP loose-detected → fail loudly, with per-shape `gh api` recipes and T2 access-pattern table) → grounded intro (Q3 verbatim) → per-item block (Q3 verbatim) → conditional >5-item triage table → tail + A3 follow-up-issue tip → orchestration walkthrough with B10 inlined batch-fetch instruction → failure modes → example invocation.
    - Ran all inspection-grade validations from the test plan (B1, B6–B10b) locally — every check PASS. Behavioral smoke (B11–B12) and the post-push registration check (B2) deferred to QA per the plan.
* Decisions made
    - Built strictly to plan. No deviations.
    - A2 (preflight v1, retained in v2): the T2 detection block explicitly anti-patterns filesystem-scanning for MCPs — detection is from the runtime registered-MCP list, not a walk of `~/.cursor/projects/*/mcps/`.
    - A3 (preflight v2): the tail emits a one-liner showing the user how to roll all "defer to follow-up" dispositions into a `gh issue create` invocation. Closes the most common post-verdict action.
* Insights
    - Build was almost entirely a transcription job, which is what a well-executed plan-and-creative phase produces. The five sequential plan revisions (Q2 reopened three times, Q3 promoted from a build sub-step to its own creative, Q4 collapsing the ruleset) front-loaded all the design risk into phases where rework is cheap.
    - The single load-bearing instruction at the top of the document (Q3 F6 — "fetch first, never judge from the URL alone") is the highest-leverage line in the file. Every other section is mechanics; that line is the corpus-attested behavior change.
