# Active Context

**Current Task:** PR Feedback Judge Command (ruleset)

**Phase:** PLAN - COMPLETE (v2 — fetch-tier strategy revised)

**What Was Done:**
- Plan v1 closed the GitHub-access question prematurely by assuming `gh` everywhere. Operator caught this — the audience is anyone with Cursor/Claude Code on any machine, including drive-by reviews of public PRs with no GitHub tooling.
- Reopened as Q2; ran a creative-generic pass; resolved as a tiered fallback chain: T1 `gh` (best, requires auth, supports private repos) → T2/T3 anonymous `curl` + `jq` or stdlib (public PRs only, 60 req/hr) → T5 harness web-fetch invoked on `api.github.com` URLs (universal floor, no shell required). T4 HTML scrape dropped as strictly dominated by T5.
- Verified T2 empirically: anonymous `curl` to `api.github.com/.../pulls/comments/<id>` returns the same JSON shape as `gh api`, with `diff_hunk` and all needed fields.
- Spliced into tasks.md: tier-agnostic API path table, per-tier invocation recipes mandate, expanded failure-mode requirements (private-repo + rate-limit messages), and tier-degraded smoke tests (B11a, B11b).
- Q1 (template wording) remains as resolved in the prior pass.

**Next Step:** Preflight phase — validate the revised plan before build.
