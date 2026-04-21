# Decision: Commit Autonomy Rule — Phrasing & Placement

## Context

Cursor's base agent prompt (injected under the `Shell` tool in a `<committing-changes-with-git>` block) contains:

> "NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive."

This reliably suppresses the commits that Niko workflows prescribe (`🚨 CRITICAL: Commit all changes…` in `level{2,3,4}-workflow` references, `/nk-save`, etc.). We need a rule that causes agents to perform those commits reliably.

**What needs to be decided**: the exact text, framing, voice, and placement of a single rule (or rule-edit) that dissolves the conflict for Niko-prescribed commits only.

**Why it matters**: this rule is the load-bearing element for every Niko workflow's phase-transition and save-point commits. If it's too weak, the base-prompt prohibition wins and agents keep hesitating. If it's too broad, agents start committing outside Niko moments (which loses the user's trust in a different way). If it adversarially "overrides" the base prompt, models that respect post-training biases toward Cursor's prompt may simply ignore the override.

**Constraints** (from `projectbrief.md` and `tasks.md`):

1. Minimal surface area — one file edit or add, not dozens.
2. Dissolves, doesn't overrides (satisfies "user explicitly asked" on its own terms).
3. Bounded scope — Niko-prescribed commits only.
4. Operator voice preferred over rule voice (per the transcript's critique).
5. Must survive `ai-rizz` sync and `a16n` cross-harness translation.
6. Must not conflict with existing `git-safety.mdc` policy (one mutating git op per turn, known inverse).

## Options Evaluated

Five candidate packages (phrasing + placement coupled, since they inform each other):

- **C1. Standalone rule, verbatim-quote framing, operator pre-auth voice.** New file `rulesets/niko/commit-autonomy.mdc`. Quotes Cursor's sentence verbatim and sets up a named exception.
- **C2. Embed in `niko-core.mdc`, generic framing, rule voice.** Adds a short section to the already-always-on core file. Does not quote Cursor; addresses the posture directly.
- **C3. Extend `git-safety.mdc`, operator pre-auth voice.** Adds a paragraph to the existing always-on git-safety rule. Semantic neighbor of mutating-git-op hygiene.
- **C4. Slash-command-as-explicit-ask reframe.** Either a standalone file or embedded in `niko-core.mdc`. Argues that invoking `/niko`, `/niko-build`, `/nk-save`, etc. *is itself* the operator's present-tense explicit request for the commits those phases prescribe. Tightest logical argument for dissolving the conflict.
- **C5. User-level rule.** `~/.cursor/rules/niko-commit-autonomy.mdc`. Applies across all the operator's Cursor workspaces. Not versioned with Niko.

## Analysis

### Comparison

| Criterion | C1: Standalone + verbatim | C2: Core-embed + generic | C3: Extend git-safety | C4: Slash reframe | C5: User-level |
|---|---|---|---|---|---|
| Files touched | 1 new | 1 edited | 1 edited | 1 new or 1 edited | 1 new (outside repo) |
| In-context priority | always-on | always-on (core) | always-on | depends on host | always-on globally |
| Ships with Niko repo | yes | yes | yes | yes | **no** |
| Directly satisfies base-prompt's condition | by pre-auth | by pre-auth | by pre-auth | **by literal slash-command act** | by pre-auth |
| Brittleness if Cursor changes prompt text | high (verbatim) | low | low | low | varies |
| Semantic fit | neutral | core ethos | git cluster | logical/elegant | neutral |
| Versioned across operator's projects | workspace only | workspace only | workspace only | workspace only | **all workspaces** |
| Bikeshed risk | moderate | moderate | moderate | low | moderate |

### Key Insights

1. **Slash-command reframing (C4) is structurally the strongest argument.** The base prompt says "commit when the user explicitly asks." When the operator types `/niko-build`, they are **literally** performing an explicit request for the commits that phase prescribes. It's not a pre-authorization ("I'll commit later") or an override ("ignore the base rule") — it's satisfying the base rule on its own terms in the present tense. Any model reasoning about whether "the user asked" has a direct, factual answer: yes, the user just typed `/niko-build`.

2. **Verbatim quoting (C1) is brittle but specific.** It creates a named exception to a named sentence, which maximally helps a model resolve the conflict — but if Cursor rewords their prompt (which happens often), the quote drifts. Generic framing (C2, C4) sidesteps this.

3. **`niko-core.mdc` already does 60% of the work.** It already emphasizes autonomous execution, "no user approval required," "meticulously follow explicit formatting constraints like commit message prefixes," and "Commitment Completeness." It does **not** currently have a direct counter to the Cursor base-prompt sentence by name. The minimum diff to get the effect is a small new section there, not a new file. This makes C2 (or C2 fused with C4's framing) the most "minimal" in the literal sense.

4. **User-level (C5) is tempting for portability but fights the goal.** If the user has many Cursor workspaces and only some use Niko, a user-level rule either scopes too broadly (risking commits in non-Niko contexts) or forces in-body scope-bounding language that's the same content as a workspace rule — just placed in a less-discoverable location. Also not discoverable by future contributors to this rules repo.

5. **`git-safety.mdc` extension (C3) mixes concerns.** The existing file is about *how* to run git ops (one at a time, with known inverse). Adding *when it's authorized to commit* is a different axis — a cleaner separation is to keep them in distinct rules.

6. **Belt+suspenders cross-references add reliability cheaply.** Adding a one-liner pointer in each `level{N}-workflow.md` reference (at the point where it says `🚨 CRITICAL: Commit all changes`) costs ~1 line × 4 files and puts the authorization in-context at the exact commit-decision moment, even if the always-on rule gets crowded out of a large context. This is orthogonal to C1–C5 and can be added to any of them.

### Candidate Wordings (rough drafts to pick from)

These are **sketches** intended for collaborative refinement with the operator, not final text.

#### C1-text (standalone, verbatim quote, operator voice)

```markdown
---
description: Pre-authorization for Niko-prescribed commits
alwaysApply: true
---

# Niko Commit Autonomy

Cursor's base instructions include:

> NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive.

I — the operator of this repository — **have explicitly asked you**, in advance, once here, and covering every future occurrence, to perform the following commits whenever you reach them inside this repo:

1. Phase-transition commits prescribed by any `level{1..4}-workflow.md` file (format: `chore: saving work before [phase] phase`).
2. Save-point commits performed by the `nk-save` skill (format: `chore: saved work on [task-id] at [phase]`).
3. Any commit whose message a Niko phase document or skill prescribes verbatim.

When any of the above applies, the condition "the user has explicitly asked" is **already satisfied by this document**. Do not re-ask. Do not interpret executing these commits as "being too proactive" — failing to perform them is the deviation from what I've asked for.

Commits outside these scenarios still require an explicit ask per Cursor's base guidance.
```

#### C2-text (embed in `niko-core.mdc`, rule voice, generic)

New section added under **Safety & Approval Guidelines**:

```markdown
- **Niko-Prescribed Commits are Pre-Authorized**: When a Niko workflow or skill file currently in your context (e.g., `level{1..4}-workflow.md`, `nk-save/SKILL.md`) prescribes a commit at a specific point with a specific message format, the operator's invocation of that workflow **is** their explicit request for that commit. Execute it without re-asking. This covers phase-transition commits and `/nk-save` save-points. Commits outside these prescribed points continue to require an explicit operator ask.
```

#### C4-text (slash-command reframe, embed in `niko-core.mdc`)

New section added under **Safety & Approval Guidelines**:

```markdown
- **Slash-Command Invocation is an Explicit Commit Request**: When the operator invokes `/niko`, `/niko-build`, `/nk-save`, or any other `/niko-*` slash command, they are **performing a present-tense, explicit request for every commit those workflows prescribe** (phase-transition commits, save-points, and any commit whose message format is given verbatim in the loaded workflow or skill). The operator typing the slash command is the explicit ask. Execute the prescribed commits without seeking fresh permission. Commits outside those prescribed moments still require an explicit ask.
```

#### Combined C2+C4 (recommended starter phrasing)

```markdown
- **Niko-Prescribed Commits are Pre-Authorized by the Slash-Command Invocation**: When the operator invokes `/niko`, `/niko-build`, `/nk-save`, or any other Niko workflow command, that invocation **is** their explicit, present-tense request for every commit the loaded workflow or skill prescribes — phase-transition commits (`chore: saving work before [phase] phase`), save-points (`chore: saved work on [task-id] at [phase]`), and any commit whose message a Niko phase document spells out verbatim. Execute these without re-asking; the explicit ask has already occurred. Commits outside these prescribed moments continue to require an explicit operator ask.
```

## Decision

**Low-Confidence Result**: The operator explicitly asked for a collaborative phrasing session — they want to pick-and-choose the wording rather than having me commit unilaterally. The structural analysis is complete and points toward a **C2+C4 hybrid** (embed in `niko-core.mdc`, slash-command-as-explicit-ask framing, with optional belt+suspenders pointers in level-workflow references), but the final text needs the operator's eye.

### Agent's recommendation (for operator to accept, modify, or reject)

1. **Placement**: embed in `rulesets/niko/niko-core.mdc` as a new bullet under **Safety & Approval Guidelines**. *Rationale*: most surgical (no new file), rides on the most-in-context always-on rule, clusters with the existing approval/autonomy language.
2. **Framing**: slash-command-as-explicit-ask (C4), optionally augmented with the pre-auth fallback language from C2 to cover Niko commits that happen without a fresh slash-command invocation (e.g., resuming a session).
3. **Verbatim quoting**: **no**. Generic framing is less brittle and the logical argument stands on its own.
4. **Belt+suspenders pointers**: **yes**, one-liner added in `level{1..4}-workflow.md` references at the `🚨 CRITICAL: Commit all changes` step. Low cost, high in-context reliability boost.
5. **User-level placement (C5)**: **not for this task**. Ships-with-Niko is a bigger win than cross-workspace portability, and future contributors/new-machine setups get it for free.
6. **Scope-bounding mechanism**: trigger-based ("when a Niko workflow or skill file currently in your context prescribes a commit") is the most robust — it auto-covers new phases/skills without maintenance, and naturally excludes non-Niko commits.

### Open to operator

1. Is the combined C2+C4 wording in the right direction, or do you prefer pure C4 (reframe only) or pure C2 (pre-auth only)?
2. Should we edit `niko-core.mdc` in place (my recommendation), or introduce a standalone `commit-autonomy.mdc` alongside it?
3. Verbatim quote of Cursor's sentence (C1 flavor) — valuable specificity or brittle liability? Do you want it as a quoted anchor or not?
4. Belt+suspenders pointers in level-workflow files — yes/no?
5. Any specific operator voice you want to hit ("I have", "I've", "I, the operator,…") or any phrasing tics (e.g., avoid the word "explicit" because it's overloaded)?
6. Escape hatch wording: current draft says "Commits outside these prescribed moments continue to require an explicit operator ask." Keep, rephrase, or drop?

## Implementation Notes (will finalize after operator decision)

- If C2/C4/hybrid: single surgical edit to `rulesets/niko/niko-core.mdc` under **Safety & Approval Guidelines**.
- If standalone file: add `rulesets/niko/commit-autonomy.mdc` with `alwaysApply: true`.
- If belt+suspenders confirmed: add one line at the `🚨 CRITICAL: Commit all changes` step in `rulesets/niko/skills/niko/references/level{1..4}/level{N}-workflow.md` and in `rulesets/niko/skills/nk-save/SKILL.md` pointing to the authorization location.
- Update `memory-bank/systemPatterns.md` with a one-bullet note under "Niko System Patterns" naming the pre-authorization mechanism so future contributors know it exists.
- Push branch so `ai-rizz` can sync on next run (`ai-rizz` reads from remote, per `techContext.md`).
