# Progress: PR Feedback Judge Command

**Complexity:** Level 3

## Summary

Build a new Cursor ruleset (`pr-feedback-judge`) that exposes a slash command for evaluating GitHub PR review feedback. The command accepts any mix of whole-PR, PR-review, and single-comment URLs; batch-fetches the relevant GitHub data via a tiered fallback chain (`gh` → anonymous `curl` + `jq`/stdlib → harness web-fetch on `api.github.com` URLs); and renders per-item "valid or invalid" verdicts using a scaffolded intro and hybrid (triage-table + valid-detail) verdict format. All tiers return identical JSON shape, so parsing and rendering are tier-agnostic. Ships as a ruleset that composes `script-it-instead` (via symlinks) so consumers who already include those rules don't get duplicates. Out of scope: `/nk-chat` (issue #63), verdict persistence.

## History

- **Niko init / intent clarification — complete.** User confirmed restated intent and clarified that ruleset composition handles the `script-it-instead` reuse concern.
- **Complexity analysis — complete.** Level 3.
- **Plan phase v1 — research & open-question identification.** Confirmed via probe: `gh` CLI installed and authenticated locally. Two of three projectbrief open questions collapsed to validated tech choices; one remained (Q1: template wording). *Defect later identified: I prematurely closed the GitHub-access question by overfitting to the local environment.*
- **Creative phase — Q1 resolved.** Scaffolded intro + hybrid verdict format. See `creative-pr-feedback-judge-template.md`.
- **Plan phase v2 — Q2 reopened and resolved.** Operator pointed out that the audience is anyone with Cursor/Claude Code on any machine, including drive-by reviews of public PRs with no GitHub tooling. Re-ran research: anonymous `curl` confirmed working against `api.github.com` (identical JSON shape, 60 req/hr anonymous limit, sufficient for one PR). Resolved as a tiered fallback chain (T1 gh → T2/T3 curl → T5 web-fetch on API URLs; T4 HTML scrape dropped as dominated). See `creative-pr-feedback-judge-fetch-tiers.md`. Plan, test plan, technology validation, and implementation steps updated to reflect tier-agnostic API path table + per-tier invocation recipes + tier-degraded smoke tests (B11a, B11b).
- **Plan phase — finalized v2.** All open questions resolved.
