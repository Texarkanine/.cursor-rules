# Progress: PR Feedback Judge Command

**Complexity:** Level 3

## Summary

Build a new Cursor ruleset (`pr-feedback-judge`) that exposes a slash command for evaluating GitHub PR review feedback. The command accepts any mix of whole-PR, PR-review, and single-comment URLs; batch-fetches the relevant GitHub data via `gh` CLI; and renders per-item "valid or invalid" verdicts using a scaffolded intro and hybrid (triage-table + valid-detail) verdict format. Ships as a ruleset that composes `script-it-instead` (via symlinks) so consumers who already include those rules don't get duplicates. Out of scope: `/nk-chat` (issue #63), verdict persistence.

## History

- **Niko init / intent clarification — complete.** User confirmed restated intent and clarified that ruleset composition handles the `script-it-instead` reuse concern.
- **Complexity analysis — complete.** Level 3.
- **Plan phase — research & open-question identification.** Confirmed via probe: `gh` CLI installed and authenticated, no GitHub MCP installed, `jq` available. URL→endpoint mapping known and unambiguous. Packaging convention confirmed via inspection of existing `script-it` ruleset and `wiggum-niko-coderabbit-pr` command (`rules/<name>.md` canonical, ruleset `commands/<name>.md` symlinks to it). Two of three projectbrief open questions collapsed to validated tech choices; one remained (Q1: template wording).
- **Creative phase — Q1 resolved.** Scaffolded intro + hybrid verdict format. See `memory-bank/active/creative/creative-pr-feedback-judge-template.md`.
- **Plan phase — finalized.** All open questions resolved; `tasks.md` is the complete implementation plan.
