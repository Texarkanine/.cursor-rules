---
task_id: md-style-and-prompt-authoring
complexity_level: 3
date: 2026-07-09
status: completed
---

# TASK ARCHIVE: Markdown Style Update & Prompt-Authoring Skill

## SUMMARY

Sharpened `rules/markdown-style.mdc` (tilde-fence nesting, no-hard-wrap rule, two heading sub-rules, broadened globs) and authored a new self-contained `prompt-authoring` skill under a new `rulesets/authoring/` group. Both deliverables shipped to plan; QA passed clean. Post-reflect, diagram guidance and a `visual-planning.mdc` symlink were added to the authoring ruleset. Post-merge, the skill canonical source settled at `rules/prompt-authoring/` with a ruleset symlink, and the authoring README was expanded to document the full ruleset.

## REQUIREMENTS

From the project brief:

### Deliverable 1: Edit `rules/markdown-style.mdc`

1. Broaden `globs` to also match `.mdc` / cursor-rule files, not only `**/*.md`.
2. Replace the "count backticks, add one" code-fence-nesting section with the tilde technique (`~~~` outer fence so inner content uses normal triple-backtick fences); keep indented blocks only as a last-resort fallback.
3. Add a "no hard wrapping" section with three-part rationale (machine-parsed ignores breaks; renderers soft-wrap; hard wraps add maintenance/diff burden).
4. Add two heading sub-rules: (a) no clarifying parentheticals; (b) short, stand-alone, nav/anchor-friendly headings.

### Deliverable 2: New self-contained prompt-authoring skill

5. Classify-what-you're-writing guidance: workflow / reference / personality, plus an explicit "none of these / composite" escape (advisory lens).
6. Skill prose must be self-contained — no references to other repo skills as examples.
7. Workflow-prompt guidance: explicit ordering for agents (numbered steps, explicit transitions, no "as above", intentional repetition, sparing load-bearing emoji).
8. Cross-reference guidance: only two acceptable cases — execution handoff; closed execution stack.
9. Prose-style guidance: Rossmann anti-slop rules mapped onto repo patterns.

### Constraints

- Canonical sources only: edit `rules/markdown-style.mdc`; new skill under `rulesets/`.
- Both artifacts must obey their own rules (worked-example constraint).
- Self-containment of Deliverable 2 is a hard constraint.

All requirements were met. Two in-scope additions came from preflight (composite worked example; convert existing tab-indented examples to tilde fences). Post-reflect operator request added diagram guidance and visual-planning symlink.

## IMPLEMENTATION

### Markdown style rule

**File:** `rules/markdown-style.mdc`

- Broadened frontmatter `globs` to `**/*.md,**/*.mdc`.
- Replaced "Markdown Code Fence Nesting" section: primary technique is `~~~` outer fences; indented blocks demoted to last-resort fallback; removed backtick-counting escalation ladder.
- Added "No Hard Wrapping" section with full rationale.
- Extended "Section Headings" with no-parentheticals and short/portable sub-rules.
- Converted existing tab-indented markdown-in-markdown examples to tilde fences so the document practices its own primary technique.
- Post-merge: description frontmatter tweak (`fix(markdown-style): make description more aggressive`).

**Ruleset assembly:** `rulesets/authoring/markdown-style.mdc` symlinks to `../../rules/markdown-style.mdc`.

### Prompt-authoring skill

**Canonical source:** `rules/prompt-authoring/SKILL.md` + `rules/prompt-authoring/references/*.md`

**Ruleset entry:** `rulesets/authoring/skills/prompt-authoring` symlinks to `../../../rules/prompt-authoring`

The plan originally placed canonical files at `rulesets/authoring/skills/prompt-authoring/`; the merged PR (#77) adopted the repo's standard assembly convention (canonical under `rules/`, symlinked into the ruleset group). Functionally equivalent and independently installable.

**SKILL.md contents:**

- Frontmatter (`name`, `description`).
- Classify lens (workflow / reference / personality + none/composite escape) with a composite worked example.
- Self-containment principle.
- Cross-reference rules (two acceptable cases).
- Prose-style section (Rossmann-derived).
- Self-check pass.
- Explicit-path pointers to `references/*.md`.

**Reference files:**

| File | Purpose |
|------|---------|
| `references/workflow-prompts.md` | Agent reads whole prompt first; explicit ordering; list semantics; repetition/omission; emoji as markers; **Diagram the Control Flow** (post-reflect) |
| `references/reference-prompts.md` | Facts/constraints; scannable; no procedure or personality |
| `references/personality-prompts.md` | Disposition/posture/defaults/voice |

**Post-reflect addition — Diagram the Control Flow:**

Added to `workflow-prompts.md`: agents read Mermaid even unrendered; pick diagram type by control-flow shape (none / flowchart / sequence); keep map (chart) separate from driving instructions (prose). Closed-stack references `visual-planning.mdc` for drawing mechanics.

**Ruleset group:**

- `rulesets/authoring/README.md` — describes the authoring ruleset; lists prompt-authoring, markdown-style, and visual-planning with links.
- `rulesets/authoring/visual-planning.mdc` symlinks to `../../rules/visual-planning.mdc`.

### Persistent file reconciliation (reflect phase)

Generalized skill-location language in persistent memory bank files:

- `memory-bank/systemPatterns.md` — from `rulesets/niko/skills/` to `rulesets/<group>/skills/`.
- `memory-bank/techContext.md` — File Conventions line for skills generalized likewise.

### Design decisions (inlined from planning)

**Skill canonical location:** All existing skills lived under `rulesets/niko/skills/` (niko-coupled). Resolved in-plan: new `rulesets/authoring/` group for general-purpose, independently installable skills. No creative phase needed — structural/naming decision, not design exploration.

**TDD applicability:** Prose deliverables have no executable units. Verification = self-consistency + QA acceptance checks + `rg` invariants. Documented honestly rather than fabricating tests.

**ai-rizz.skbd registration:** Flagged as deployment follow-up, out of scope for content authoring.

### Key commits

| Commit | Description |
|--------|-------------|
| `ad91bed` | Main deliverable: markdown-style rewrite + prompt-authoring skill (#77) |
| `4046eed` | Authoring README improvements |
| `a795a62` | Authoring README link fixes |
| `b0bea9a` | Markdown-style description tweak |

## TESTING

No automated test framework (prose/ruleset project). Verification performed:

### Preflight (PASS w/ advisory)

- TDD encoding: PASS — prose deliverables, documented substitute verification.
- Convention: PASS w/ note — new `rulesets/authoring/` extends skill-location pattern.
- Dependency: noted — `ai-rizz.skbd` registration is deployment follow-up.
- Conflict: PASS — convert existing indented examples to tilde fences.
- Completeness: PASS — all 9 requirements mapped to steps.

### QA (PASS)

All 10 acceptance checks passed:

- markdown-style frontmatter globs match `.md` and `.mdc`.
- Code-fence section teaches `~~~` technique; indented blocks demoted; backtick ladder removed.
- No-hard-wrap section with three-part rationale.
- Heading sub-rules present.
- Skill exists with frontmatter; classify lens includes composite escape.
- Zero sibling-skill references in skill prose (`rg` clean).
- Cross-reference section lists exactly two acceptable cases.
- Prose-style section adopts Rossmann rules.
- Both artifacts obey markdown-style.mdc themselves.

Manual checks: no em-dashes, no linter errors, tilde fences render cleanly.

## LESSONS LEARNED

### Technical

- A document that teaches a fencing technique must use that technique on itself, which forces the meta-case (showing the fence character itself) into prose rather than demonstration.
- When a task is the first instance of a pattern (non-niko skill location), persistent files describing the old singular reality need generalizing at reconcile — catch at reflect, not by leaving docs accidentally narrow.
- Treating "self-contained" as a grep-able invariant (`rg` for sibling-skill names) made a fuzzy requirement mechanically checkable.

### Process

- Preflight earned its keep: caught the consistency gap (rule's own examples demonstrating the soon-to-be-demoted fallback) before build, turning a likely QA finding into a planned build step.
- Encoding soft constraints as `rg` checks is cheap and worth doing whenever the constraint has a detectable signature.
- The workflow reference's diagram section is a worked example of the skill's own cross-reference rule: co-located controlled artifact, referenced for mechanics, section still complete on its own.

## PROCESS IMPROVEMENTS

- When a task introduces the first instance of a repo pattern (e.g., a non-niko ruleset group), include explicit reconcile checklist items for `systemPatterns.md` and `techContext.md` in the plan rather than deferring to reflect advisory.
- Preflight "practice what you preach" checks (does the rule demonstrate its own primary technique?) should be standard for meta-rules about formatting.

## TECHNICAL IMPROVEMENTS

- **ai-rizz.skbd registration:** Add `rulesets/authoring` entry so the new group is installable via `ai-rizz` without manual symlink setup. Deferred as deployment follow-up.

## NEXT STEPS

- Register `rulesets/authoring` in `ai-rizz.skbd` when ready to make the group installable via standard tooling.

## INLINED EPHEMERAL CONTENT

### Project Brief (original)

**User story:** As the author/maintainer of this rules repository, sharpen the Markdown styling rule and add a self-contained prompt-authoring skill so anything written in this repo (and installed elsewhere) follows consistent, defensible conventions.

**Use cases:** (1) Authoring Markdown in this repo; (2) Authoring a prompt, rule, or skill without assuming co-installed artifacts.

### Progress history

**2026-06-11 — COMPLEXITY-ANALYSIS — COMPLETE**

- Cleared stale task state (#76); confirmed two-deliverable scope; classified L3.
- Open question: canonical skill location for non-niko skill — resolved in Plan.

**2026-06-11 — PLAN — COMPLETE**

- Mapped components; wrote full L3 plan into `tasks.md`.
- Decision: new `rulesets/authoring/` group; per-type guidance in `references/`.
- TDD N/A for prose; verification = self-consistency + QA + `rg`.

**2026-06-11 — PREFLIGHT — COMPLETE (PASS w/ advisory)**

- Validated plan; wrote `.preflight-status`.
- Tweaks: composite worked example; build note to convert indented examples to tilde fences.

**2026-06-11 — BUILD — COMPLETE**

- Rewrote `markdown-style.mdc`; created `rulesets/authoring/` group with skill + references.
- Wrote all prose unwrapped; `rg` confirms skill free of repo-specific names.

**2026-06-11 — QA — COMPLETE (PASS)**

- All 10 acceptance checks pass; no fixes required.

**2026-06-11 — REFLECT — COMPLETE**

- Wrote reflection; reconciled `systemPatterns.md` and `techContext.md`.

**2026-06-11 — POST-REFLECT ADDITION (operator request)**

- Added "Diagram the Control Flow" to `workflow-prompts.md`.
- Symlinked `visual-planning.mdc` into authoring ruleset.

### Reflection (full)

**Summary:** Both deliverables shipped to plan; QA passed clean.

**Requirements vs outcome:** All nine requirements delivered. Preflight additions (composite example; tilde-fence conversion) in-scope.

**Plan accuracy:** File list and step order held. Skill location resolved in-plan without creative phase — proportionate for a directory-structure choice.

**Creative phase:** Not invoked. Structural decision, not design exploration.

**Build & QA:** Fencing the rule file correctly was the main care point. QA clean first time because self-containment was a hard constraint throughout build.

**Cross-phase:** Preflight converted a likely QA finding into a planned build step. TDD applicability correctly classified so no fabricated tests.

**Insights:**

- Meta-rules about markdown fencing constrain the document to demonstrate its primary technique; meta-case goes in prose.
- First instance of a pattern requires persistent-file generalization at reconcile.
- Grep-able invariants for soft constraints (self-containment) are cheap and effective.

### Creative phase

No creative phase was invoked for this task. The single open question (skill canonical location) was a structural/naming decision resolved during planning.
