# Active Context

**Current Task:** PR Feedback Judge Command (ruleset)

**Phase:** PLAN - COMPLETE (v3 — fetch-tier reordered, warehouse-mining baked into build)

**What Was Done:**
- Q2 re-revised after operator feedback: tier order is now **T0 GitHub MCP → T1 `gh` CLI → T2 anonymous `curl` (best-effort)**. Anonymous demoted to third-class with no rate-limit engineering and explicitly no env-var token harvesting (per operator constraint).
- Sanity-check / count-verification step rejected — long-list truncation is a user-behavior fix (use a more specific URL), not an engineering concern.
- Q1 reclassified as provisionally resolved (v0). Build Step 1 is now an explicit warehouse-mining task: re-read `memory-bank/cursor_pull_request_feedback_references.md` deliberately, run `cw-query` SQL to extract the actual first-user-prompt and URL-bearing-message text from the ~40 PR-feedback sessions in the local warehouse (XML-stripped via `regexp_extract` on `<user_query>`), run `cw-recall` semantic searches for paraphrases, synthesize the recurring framing/criteria/structure the user actually uses, and amend the template if v0 misses or overfits. The post-mining template is the final Q1 resolution.
- `creative-pr-feedback-judge-fetch-tiers.md` rewritten end-to-end. `tasks.md` updated: tier ordering, removed sanity-check angle, added build Step 1 warehouse-mining ahead of command-body write, smoke tests adjusted (B11a now T2-only, B11b expects "install gh / register MCP" message).

**Next Step:** Preflight phase — validate the v3 plan before build.
