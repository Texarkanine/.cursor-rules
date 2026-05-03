# Progress: PR Feedback Judge Command

**Complexity:** Level 3

## Summary

Build a new Cursor ruleset (`pr-feedback-judge`) that exposes a slash command for evaluating GitHub PR review feedback. The command accepts any mix of whole-PR, PR-review, and single-comment URLs; batch-fetches the relevant GitHub data via a tiered chain that prefers a registered GitHub MCP server, falls back to authenticated `gh` CLI, and finally to anonymous `curl` (best-effort, public PRs only); and renders per-item "valid or invalid" verdicts using a scaffolded intro and hybrid (triage-table + valid-detail) verdict format. The intro/verdict template is provisional v0 — it gets validated and possibly amended in build Step 1 against the actual user-prompt corpus mined from the local Cursor warehouse, not just the summary doc handed in at task kickoff. Ships as a ruleset that composes `script-it-instead` (via symlinks). Out of scope: `/nk-chat` (issue #63), verdict persistence, env-var token harvesting.

## History

- **Niko init / intent clarification — complete.** User confirmed restated intent and clarified that ruleset composition handles the `script-it-instead` reuse concern.
- **Complexity analysis — complete.** Level 3.
- **Plan phase v1 — research & open-question identification.** *Defect: I prematurely closed the GitHub-access question by overfitting to my locally-authenticated `gh`.*
- **Creative phase — Q1 resolved (v0).** Scaffolded intro + hybrid verdict format. See `creative-pr-feedback-judge-template.md`.
- **Plan phase v2 — Q2 reopened.** Operator pointed out the audience reality: anyone with Cursor/Claude Code on any machine, including drive-by reviews. First Q2 resolution proposed an T1→T2/T3→T5 chain with significant anonymous-tier engineering.
- **Plan phase v3 — Q2 re-revised + Q1 grounding requirement added.** Operator pushed back further:
  - Anonymous is third-class; most real users will be logged in. Tier order should be **MCP → CLI → anonymous**, with anonymous as best-effort and no env-var token harvesting.
  - No sanity-check / count-verification step needed — long-list truncation is a "use a more specific URL" problem for the user, not an engineering problem for us.
  - Q1's v0 template is grounded in the warehouse summary doc, not in the actual user-prompt corpus. Build phase must explicitly include reading the summary and running `cw-query` / `cw-recall` queries to extract the user's real questioning patterns, then refine the template.
  - All three points integrated: `creative-pr-feedback-judge-fetch-tiers.md` rewritten with T0→T1→T2 ordering and explicit "no env-var grovel" / "no sanity-check" decisions; `tasks.md` got a new build-phase Step 1 (warehouse mining) before the command-body write.
- **Plan phase — finalized v3.** All open questions resolved (Q1 final answer deferred to build Step 1 by design).
