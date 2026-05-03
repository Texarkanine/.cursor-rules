# Active Context

**Current Task:** PR Feedback Judge Command (ruleset)

**Phase:** PLAN - COMPLETE (v4 — tier order flipped, anonymous cut, Q3 grounded template done)

**What Was Done:**
- Q2 reopened a third time after operator added a real GitHub MCP server (`user-github`, 41 tools) to the harness. Inspection confirmed: this MCP — and likely most read-oriented GitHub MCPs — has only PR/issue-scoped method-dispatch tools; no single-comment-by-ID getter. That flips the tier order: T1 `gh` is now preferred (O(1) single-comment lookups + native batching with `script-it-instead`); T2 GitHub MCP is fallback (loose-detected via case-insensitive `github` substring match against server metadata). Anonymous access cut entirely. No env-var token harvesting. Failure when neither tier present is a clear "install gh / register MCP" message.
- Q3 promoted from a build step to its own creative exploration. Did the actual mining: extracted 21 URL-bearing user prompts from the local Cursor warehouse via `cw-query` SQL, filtered to 12 clean signals, synthesized six findings (F1–F6) about the user's real questioning patterns. The corpus revealed v0's criteria vocabulary was wrong ("technical accuracy / severity / scope alignment" → user actually says "valid / worth fixing / in scope for this PR"), v0 collapsed three questions the user wants separate, v0 missed the disposition concept, v0 over-optimized for 30-item runs that don't appear in the corpus, and v0 missed a corpus-attested failure mode (agent judging before fetching). Final template in `creative-pr-feedback-judge-template-grounded.md`; v0 banner-marked superseded.
- Plan revised: implementation plan now 5 build-execution steps. Tier-detection block, URL→endpoint table, README dependency line, and smoke-test expectations all updated for the gh→MCP order.

**Next Step:** Preflight phase — validate the v4 plan before build.
