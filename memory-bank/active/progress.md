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
