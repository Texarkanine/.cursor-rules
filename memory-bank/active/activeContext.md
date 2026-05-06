# Active Context

**Current Task:** Add `/niko-chat` ad-hoc entrypoint (issue #63)

**Phase:** BUILD - COMPLETE

**What Was Done:**
- Created `rulesets/niko/skills/niko-chat/SKILL.md` (new) — read-only memory-bank-aware Q&A skill with 5 numbered steps, explicit Non-Goals, graceful degradation paths, and structured "Context Loaded" greeting (the within-scope improvement identified in preflight).
- Updated `rulesets/niko/README.md`:
  - Added `### Naming Convention: niko-* vs nk-*` subsection above "Circuit Breakers" documenting the namespace split.
  - Added `#### Codebase Chat` subsection under "Ad-Hoc Entrypoints" documenting `/niko-chat` with its three use-cases and the read-only contract.

**Files Created/Modified:**
- `rulesets/niko/skills/niko-chat/SKILL.md` (created)
- `rulesets/niko/README.md` (modified)

**Key Decisions During Build:**
- Placed naming-convention subsection above Circuit Breakers (not as a new top-level section) so the existing structure flows into it naturally.
- Frontmatter `description:` is unusually long for a skill — deliberately so. Skill descriptions are how the agent decides whether to invoke a skill; for `niko-chat` the trigger conditions are nuanced (chat-not-do, parallel-or-standalone) and need to be in the description so the agent picks it up correctly without false positives or misses.
- Added explicit "When to Use This vs. Other Entrypoints" section in the skill body to head off `/niko-chat` getting invoked when `/niko` or `/niko-creative` is the right tool.

**Deviations from Plan:**
- None — built to plan, with the preflight-flagged structured-context-summary requirement folded into Step 2 of the skill body.

**Next Step:** QA phase will run automatically.
