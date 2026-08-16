# Progress

Expand the two existing writing-style decompression keys into a four-style family (always-respond, always-write, ManualPrompt skill) and a `writing-styles` ruleset that ships only the skills, with a README sample table left as placeholders.

**Complexity:** Level 2

## 2026-08-16 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Validated intent: four slugs, three flavors, ruleset name `writing-styles`, Thomas and Turner credit, Cursor `disable-model-invocation: true`
    - Classified Level 2 (self-contained enhancement; existing ruleset-assembly pattern)
* Decisions made
    - Always-on respond/write files stay a la carte under `rules/`; ruleset is skills-only
    - Do not harvest `claude -p` samples by moving `~/.claude` trees
* Insights
    - Same shape as the ISO 24495 L2: decompression keys plus layout checks; this task adds a ruleset and rename
