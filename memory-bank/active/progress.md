# Progress: PR Feedback Judge Command

**Complexity:** Level 3

## Summary

Build a new Cursor ruleset (`pr-feedback-judge` or similar) that exposes a command for evaluating GitHub PR review feedback. The command accepts any mix of whole-PR, PR-review, and single-comment URLs; batch-fetches the relevant GitHub data via the best-available access path; and renders per-item "valid or invalid" verdicts using the user's standard questioning/evaluation intro. Ships as a ruleset that composes `script-it-instead` to avoid duplication for consumers who already include it. Out of scope: `/nk-chat` (issue #63), verdict persistence.

## History

- **Niko init / intent clarification — complete.** User confirmed restated intent and clarified that ruleset composition handles the `script-it-instead` reuse concern.
- **Complexity analysis — complete.** Level 3.
