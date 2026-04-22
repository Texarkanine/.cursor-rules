# Decision: Commit Autonomy Rule — Phrasing & Placement

## Context

Cursor's base agent prompt contains an always-on injection that causes agents to skip Niko-prescribed commits:

> "NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive."

(Full diagnostic: `memory-bank/active/cursor_request_for_system_prompt_detail.md`.)

**What needs to be decided**: the exact text, framing, voice, and placement of the Niko-side guidance that causes agents to reliably perform the commits prescribed by `level{1..4}-workflow.md` phase transitions and by `/nk-save`.

### Design shift after operator feedback (v2)

The operator pushed back on framing the rule as a *patch against Cursor's prompt*. Niko shouldn't be polluted with idiosyncratic responses to one harness's current wording — that ages badly and signals the wrong intent. The rule should instead be a **general Niko principle** that happens to also resolve the observed Cursor behavior:

> **Workflow invocation is the operator's explicit consent for every action that workflow prescribes.** Harness safeguards that defer to "explicit user requests" are satisfied by the invocation itself.

This framing:

- Is stable across harnesses (Claude Code, future Cursor, anything else) because it doesn't target a specific injected sentence.
- Generalizes beyond commits (covers any prescribed action a harness might gate on).
- Positions the principle as *what Niko is*, not *what Niko defends against*.

### Empirical failure mode to design against

Observed: agents running a *sub*-slash-command like `/niko-build` were reasoning that "the operator typed `/niko-build`, not `/niko`, so this isn't the full explicit-consent invocation." Sub-command invocation was not being recognized as inheriting consent from the top-level workflow it's part of. **This is the specific failure mode the rule needs to address**, and it implies the consent affirmation needs to be visible at the invocation site for each sub-command, not just at the `/niko` root.

### Constraints

1. Minimal surface area preferred, but effectiveness ≥ minimalism when they conflict (operator's "minimal but effective").
2. Framing is a general Niko principle, not a Cursor-specific patch.
3. Scope bounded to what a Niko workflow/skill explicitly prescribes — not a license for arbitrary side actions.
4. Must survive `ai-rizz` sync and `a16n` cross-harness translation.
5. Must not conflict with existing `git-safety.mdc` (one mutating git op per turn, known inverse).
6. Sub-command invocation must be handled as equivalent-consent to the parent workflow.

## Options Evaluated

Each option gets a prose name for ease of reference.

- **C1 — Named Exception**: New standalone file `rulesets/niko/commit-autonomy.mdc`, always-on. Quotes Cursor's offending sentence verbatim and creates a named exception. Cursor-specific by construction.
- **C2 — Core Bullet**: Short bullet added to `rulesets/niko/niko-core.mdc` under **Safety & Approval Guidelines**. Already-always-on, generic framing, smallest net-new content for a single-file solution.
- **C3 — Git-Safety Extension**: Paragraph added to `rulesets/niko/git-safety.mdc`. Clusters with the existing git-ops-hygiene rule.
- **C4 — Invocation-As-Consent (global)**: A rule (placement flexible — standalone or inside `niko-core.mdc`) that reframes slash-command invocation as the present-tense explicit ask. Could be commit-specific or (v2 form) a general-principle statement about workflow invocation.
- **C5 — User-Level Global**: `~/.cursor/rules/niko-commit-autonomy.mdc`. Applies across all the operator's Cursor workspaces. Not versioned with Niko repo.
- **C6 — Per-Workflow Header**: A consent affirmation lives *inside each Niko file that prescribes a commit* (4 level-workflow references + `nk-save/SKILL.md`). The affirmation travels with the instruction; no reliance on always-on injection being respected.

### C6 variants

- **C6a — Per-Workflow Header, Inline Full Text**: Full authorization paragraph embedded at the top of each of the 5 files. Maximum in-context strength; highest drift risk (5 copies).
- **C6b — Per-Workflow Header, Shared Load**: Short `Load: <path-to-consent-ref>` directive at the top of each of the 5 files, pointing to one canonical consent reference (e.g., `rulesets/niko/skills/niko/references/core/invocation-consent.md`). One source of truth; five tiny pointers.
- **C6c — Per-Command Header (broader)**: Header on **every** `/niko-*` and `/nk-*` SKILL.md, not just the ones that directly commit. Addresses the observed sub-command failure mode (`/niko-build` not recognized as inheriting from `/niko`) by asserting consent at every invocation surface. Maximum coverage; most files touched (~10).
- **C6d — Niko-Core + Per-Workflow (hybrid)**: C2-style bullet in `niko-core.mdc` **plus** C6a or C6b headers. General posture in core; specific affirmation at commit site. Belt + suspenders.

## Analysis

| Criterion | C1 Named Exception | C2 Core Bullet | C3 Git-Safety Ext | C4 Invocation-As-Consent | C5 User-Level | C6a Per-File Full | C6b Per-File Load | C6c Per-Command Hdr | C6d Hybrid |
|---|---|---|---|---|---|---|---|---|---|
| Files touched | 1 new | 1 edit | 1 edit | 1 new or 1 edit | 1 new (outside repo) | 5 edits | 5 edits + 1 new | ~10 edits | 1 edit + 5 edits + 1 new |
| Framing | Cursor-specific | can be generic | git-clustered | generic (v2) | varies | generic | generic | generic | generic |
| Addresses sub-command failure mode | no | no | no | partial | no | yes (4 of 5 hits) | yes | **yes (best)** | yes |
| Reliance on always-on injection | full | full | full | full | full | **none** | **none** | **none** | partial |
| Maintenance burden on phrasing changes | 1 file | 1 file | 1 file | 1 file | 1 file | 5 files | 1 file | ~10 files | varies |
| Addresses operator's "not a Cursor patch" goal | poor | yes | partial | **yes** | varies | **yes** | **yes** | **yes** | **yes** |
| Portability across future harnesses | poor | fair | fair | **good** | fair | **good** | **good** | **good** | **good** |

### Key Insights (updated)

1. **C1 is now explicitly off the table**. It bakes Cursor's current sentence into Niko, which violates the "don't patch idiosyncrasies" goal.

2. **Sub-command failure mode changes the calculus**. If agents are empirically reasoning "`/niko-build` ≠ `/niko`, so no explicit consent," a single always-on rule in `niko-core.mdc` may not reach into that reasoning; it lives in a different mental slot than the thing the agent is actively reading. The fix is to assert consent at each sub-command's invocation surface — which is C6c in its purest form.

3. **Generic-principle framing decouples the fix from the problem's shape**. If Claude Code or a future Cursor rewrite has a different caution prompt, the Niko rule still applies on its own terms (as a Niko principle about workflow invocation) rather than needing to be re-targeted.

4. **C6b (shared Load) is the drift-proof version of C6**. One canonical file carries the text; 5 tiny one-line directives pull it in at load time. Phrasing iteration only touches the canonical file. It gets most of C6a's strength for almost none of C6a's maintenance cost.

5. **C2 and C6 are complementary, not competing**. C2 states the general Niko posture always-on; C6 hits each sub-command's reading frame. Together (C6d) they reinforce without redundancy: the core bullet sets "this is a Niko value," the per-file headers say "and it applies specifically to this invocation." This is the most likely-to-work option; it's also the second-most-files-touched.

6. **`ai-rizz` reads from remote**. Any option that adds/edits files must be pushed before local `.cursor/rules/` reflects the change. Noted as a pre-canary step.

### Candidate Wordings (v2, generic-principle framing)

#### Canonical consent statement (for C2 bullet, C6a inline, or C6b `Load:` target)

```markdown
## Workflow Invocation is Explicit Consent

Niko workflows and skills prescribe specific actions at specific points — phase-transition commits, save-point commits, file writes within the declared scope, and other actions spelled out in the workflow's instructions. When the operator invokes a Niko workflow or skill (by name, by slash command including sub-commands like `/niko-build` or `/nk-save`, or by resuming an in-progress workflow), that invocation is their **explicit, present-tense consent for every action the workflow prescribes**.

Default harness safeguards that require an "explicit user request" for particular action types (git commits, shell execution, file edits, etc.) are **satisfied by the operator's invocation of the workflow** — they do not require a fresh, separate ask for each prescribed action. Sub-command invocation (`/niko-build`, `/niko-plan`, etc.) inherits consent from the parent workflow it implements; the sub-command is itself a first-class explicit ask.

Execute the prescribed actions without seeking fresh authorization. Failing to execute a prescribed action is the deviation from what the operator has asked for.

Actions *outside* what the workflow explicitly prescribes still require an explicit operator ask, as normal.
```

#### C2 Core-Bullet form (compact, for embedding in `niko-core.mdc`)

```markdown
- **Workflow Invocation is Explicit Consent**: When the operator invokes a Niko workflow or skill — by slash command (including sub-commands like `/niko-build` or `/nk-save`), by name, or by resuming an in-progress workflow — that invocation is their explicit, present-tense consent for every action the workflow prescribes (phase-transition commits, save-points, in-scope edits, etc.). Default harness safeguards that gate on "explicit user request" are satisfied by the invocation itself; do not seek fresh authorization for prescribed actions. Failing to execute a prescribed action is the deviation from what the operator asked for. Actions outside what the workflow prescribes still require an explicit ask.
```

#### C6b short-form header (one-liner at top of workflow/skill files)

A block like this appears at the top of each of: `level{1..4}-workflow.md`, `nk-save/SKILL.md`, and optionally every `/niko-*` SKILL.md:

```markdown
> **Invocation is Explicit Consent.** Loading this workflow is the operator's explicit request for every action it prescribes (including commits). Harness safeguards that gate on "explicit user request" are satisfied by the invocation. See `.cursor/skills/shared/niko/references/core/invocation-consent.md` for the full principle.
```

Or even tighter, if you prefer:

```markdown
> **By loading this, the operator has explicitly requested every action it prescribes.** Harness "explicit user request" safeguards are already satisfied. Full principle: `<path>`.
```

## Decision

**Low-Confidence Result** — operator is selecting phrasing collaboratively.

### Agent's recommendation (updated v2)

**C6d — Niko-Core + Per-Workflow Hybrid, with `Load:`-directive variant (C6b mechanism for the per-file piece)**. Specifically:

1. **Add** the "Workflow Invocation is Explicit Consent" bullet to `rulesets/niko/niko-core.mdc` under **Safety & Approval Guidelines** (C2 form, compact).
2. **Add** a canonical reference file at `rulesets/niko/skills/niko/references/core/invocation-consent.md` (or similar) containing the full principle statement. Plain Markdown, no frontmatter, per the post-migration reference convention.
3. **Add** a short header block at the top of each of:
   - `rulesets/niko/skills/niko/references/level1/level1-workflow.md`
   - `rulesets/niko/skills/niko/references/level2/level2-workflow.md`
   - `rulesets/niko/skills/niko/references/level3/level3-workflow.md`
   - `rulesets/niko/skills/niko/references/level4/level4-workflow.md`
   - `rulesets/niko/skills/nk-save/SKILL.md`
   
   — with a short affirmation + `Load:` pointer to the canonical reference.
4. **Optional stretch**: extend C6 to every `/niko-*` SKILL.md (C6c coverage) to directly neutralize the observed sub-command failure mode even when no level-workflow reference is loaded yet. ~5 additional files, all tiny edits.

Total: 1 `niko-core.mdc` edit + 1 new reference file + 5 tiny header additions (or ~10 if including 4-stretch). Phrasing iteration only touches 1 file (the canonical reference + the core bullet — which should say substantively the same thing in different form).

### What's traded away

- **Minimalism by file count**: 7 files vs. 1. That's the cost of defense-in-depth against a known failure mode.
- **One extra `Load:` step** during workflow execution (negligible cost).

### Why this wins over single-file options

- **C2 alone** doesn't address the `/niko-X ≠ /niko` sub-command failure mode because the core bullet, while always-on, lives in a different part of the agent's attention than the SKILL/workflow file it's currently executing.
- **C6b alone** covers the invocation site but misses the "this is the general Niko posture" message that a core-level bullet conveys.
- Together, the core bullet sets expectations, the per-file headers enforce them at the point of use.

## Open to operator (updated questions)

1. **Is the v2 "Workflow Invocation is Explicit Consent" general-principle framing the right center of gravity?** (Alternative: narrower commit-only framing.)
2. **Do you want the full recommendation (C6d hybrid), or a subset?**
   - C6d full: core bullet + canonical reference file + 5 workflow/skill headers
   - C6d minus headers: just the core bullet + canonical reference (drops the per-file fix against sub-command failure)
   - C6b only: canonical reference + 5 headers, no core bullet
   - C6c stretch: C6d + extend headers to all `/niko-*` SKILL.mds (~10 total header sites)
3. **Canonical-reference file placement**: `rulesets/niko/skills/niko/references/core/invocation-consent.md` (under the niko skill references, fits the existing taxonomy) or somewhere else?
4. **Voice and phrasing on the canonical statement**: any nits on the draft above? (e.g., too long, too short, wrong tone, operator-first-person vs. third-person, prefer "explicit consent" vs. "explicit request" vs. something else?)
5. **Short-form header wording**: prefer the more-explanatory "Invocation is Explicit Consent…" block or the tighter "By loading this…" one-liner?
6. **Escape hatch**: current draft keeps "Actions outside what the workflow prescribes still require an explicit ask." Keep, tighten, or drop?
7. **Sub-command stretch (C6c)**: apply the header to every `/niko-*` SKILL.md, or only the commit-prescribing ones?

## Implementation Notes (will finalize after operator decision)

- If C6d or C6c is chosen, structural sync path: new file under `rulesets/niko/skills/niko/references/core/` → gets synced into `.cursor/skills/shared/niko/references/core/` by `ai-rizz`.
- Header edits are tiny and localized; verify nothing breaks existing `Load:` path references with a grep check (`scripts/migrate_manual_rules.py verify`-style).
- `a16n` sandbox translation should handle the new reference cleanly (post-migration resource paths are handled per the known caveat in the recent archive).
- Push branch so `ai-rizz` picks up changes on next run.
- Update `memory-bank/systemPatterns.md` with a one-bullet mention of the "Invocation is Consent" principle under Niko System Patterns for future-contributor discoverability.
