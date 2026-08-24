---
task_id: txrk9-pr-review
complexity_level: 2
date: 2026-08-24
status: completed
---

# TASK ARCHIVE: txrk9-pr-review

## SUMMARY

Landed the TXRK9 PR Review prompt as a ManualPrompt skill so Other findings actually get published, without turning the reviewer into a nit bot. Canonical file is [rules/txrk9-basic-pr-review/SKILL.md](https://github.com/Texarkanine/.cursor-rules/blob/better-pr-review/rules/txrk9-basic-pr-review/SKILL.md) (moved off the planned `rules/pr-review/` path). Draft PR: [#118](https://github.com/Texarkanine/.cursor-rules/pull/118).

## REQUIREMENTS

- Canonicalize the existing automation prompt under `rules/`, pasteable from the H1 down, no ruleset, no merge with `pr-feedback-judge`.
- Keep Critical, the 1–4 cascade, 🦮 body, cap of 6, neighborhood / already-owned filters, and silence after a real Other cull.
- Raise Other: named edges, lockstep misses, and tests that would still pass — not nits, not a quota, not few-shots.
- Name posting as actions, not Cursor tool identifiers.

## IMPLEMENTATION

Copied the operator's then-current prompt, then applied planned Other-sensitivity edits: retargeted silence; closed Hunt Other list after Q2 and Q3 yes; split the stronger-author omit so it no longer kills Other. Post-reflect: tool names became actions; mermaid rewired so Q4-no hunts Other and approve-versus-comment happens before the single post (the automation's own inline on #118); Hunt Other restatement under Comment shape was dropped as map re-narration. Frontmatter `name` is still `pr-review`. No REUSE or generated-tree edits.

## TESTING

No new automated tests (prose/policy). `make test` passed (ruleset symlink + README link checks; unaffiliated skill is a no-op there). `/niko-preflight` PASS WITH ADVISORY. `/niko-qa` PASS (mermaid mismatches were advisory; they were later fixed on the PR). Live proof is the next automation paste, not a change-detector on prompt text.

## LESSONS LEARNED

- Other was already a class. Live TXRK9 reviews were almost all approve-with-zero-inlines because of an unqualified "silence is success" opener and a "prove the claim / stronger author" omit written for a real-harm-only product. The cap of 6 was never the bottleneck.
- A corpus of those reviews beat guessing which sentence to change.
- A mermaid map that disagrees with Hunt Other prose will get posted as an Other finding by this same prompt. Numbered prose is the driver; keep the chart in lockstep.

## PROCESS IMPROVEMENTS

L2 locked a second Other pass. Preflight advised folding the closed list into Q3 instead. That tighter shape is still available if the extra pass proves noisy.

## TECHNICAL IMPROVEMENTS

If Other had been a duty in the first draft, the closed list would live in Q3's Other branch rather than a second workflow. What shipped is that design plus the extra pass the plan required.

## NEXT STEPS

- Merge [PR #118](https://github.com/Texarkanine/.cursor-rules/pull/118).
- Paste from the H1 in `rules/txrk9-basic-pr-review/SKILL.md` into the Cursor automation system prompt (automations do not load skills).
- Watch the next few TXRK9 reviews for Other inlines that are not nits.
