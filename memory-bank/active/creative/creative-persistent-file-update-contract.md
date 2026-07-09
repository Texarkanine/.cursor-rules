# Decision: Persistent-File Update Contract

## Context

**What needs to be decided:** How to amend the persistent memory-bank guidance rules (`rulesets/niko/niko/memory-bank/systemPatterns.mdc`, and possibly `productContext.mdc` / `techContext.mdc`) so that an agent who encounters a memory-bank persistent file *outside* the Niko workflow — but who does pick up the glob-attached rule — understands that the file is essentially read-only to them unless their work invalidated something in it. Includes resolving a stated tension: should each rule refer to `reconcile-persistent.md` as "here's how to think about this," or carry the judgment itself?

**Why it matters:** The persistent files are the highest-leverage context artifacts in the system — they are read at the start of every Niko phase. Accretion destroys them: once a file becomes an append-only mirror of recent work, the signal drowns, reading cost explodes, and reconciliation becomes impossible because everything looks load-bearing.

**Constraints:**

- Amendments must be minimal — surgical additions, not rewrites.
- Must comply with `markdown-style.mdc` (short portable headings, no hard wrap) and the prompt-authoring skill (reference-kind prose, cross-reference discipline, no filler, reserved absolutes).
- Must work for the out-of-workflow audience: an agent with no Niko context, no reconcile step, and no guarantee that any other Niko file is installed or findable.
- Must not break the in-workflow flow: `reconcile-persistent.md` already defers to these rules for content definition ("Load its guidance rule — this defines what belongs in the file").

## The Failure Mode: Persistent-File Accretion

Named and characterized, from the two observed failures (zbcli `systemPatterns.md`; FoxForge-GG `AGENTS.md`):

1. **Trigger.** The rule glob-attaches whenever *any* agent touches the file, but every verb in the rule is about creation. There is no update contract, so the agent falls back on its default prior: "I just finished work; good practice is to document it; here is the project's documentation file."
2. **Invitation.** The rule's own text feeds the prior: "this document can be appended to later as actual work reveals patterns" reads, to a task-completing agent, as *now is later, and my work revealed things*.
3. **Filter mismatch.** The "Avoid" list (obvious / ordinary / temporal) filters **triviality**. The glommed content is none of those — the zbcli `dev forward` registry paragraph is non-obvious, exceptional, and permanent. It fails on a dimension the rule never names: **altitude**. It documents one subsystem's runtime mechanics (a design doc / feature spec) rather than a pattern someone must know before touching *other* parts of the system.
4. **End state.** Each task appends its own residue and the file drifts from "senior developer's briefing" to "append-only mirror of the codebase." FoxForge is the terminal case: an entire architecture encyclopedia — UI walkthroughs, component tables, per-feature mechanics — under a "patterns" heading.

Shorthand: **session residue at the wrong altitude, accreting because the rule defines creation but not stewardship.**

## Options Evaluated

- **A — Path-reference to reconcile-persistent:** each rule adds "when updating, follow `.cursor/skills/shared/niko/references/core/reconcile-persistent.md`."
- **B — Inline update contract:** each persistent rule gains a compact "When to Update" section distilling reconcile-persistent's judgment (invalidation-only, surgical, skip confidently); `systemPatterns.mdc` additionally gains an altitude test in its "Avoid" list.
- **C — Shared companion rule:** one new rule, glob-matched to all three persistent files, holding the common update contract.
- **D — Guard line in the generated files:** amend the templates so each generated `.md` carries a "maintained by reconciliation; edit only to correct invalidated content" notice.

## Analysis

| Criterion | A: path reference | B: inline contract | C: companion rule | D: template guard |
|-----------|-------------------|--------------------|-------------------|-------------------|
| Reaches the failing audience | Only if the path resolves | Yes — glob attach is exactly the trigger | Yes, if co-installed | Yes, even rule-less agents |
| Survives installation variance | No — path differs per consumer layout and per harness (a16n) | Yes — self-contained | Weak — a fourth file must ship alongside | Yes — travels with the file |
| Prompt-authoring compliance | Violates cross-reference rule (content reference, not execution handoff) | Clean | Clean per file, but breaks self-containment of the set | N/A (artifact, not prompt) |
| Drift risk | Low (single source) but replaced by broken-link risk | Small, deliberate, grep-verifiable | Moderate (rule ↔ rule coordination) | Low |
| Minimality | Smallest diff | Small diff × 3 rules | New file + wiring | Template change; existing files unpatched |

Key insights:

- **The rules are the shared authority; reconcile-persistent already points back at them.** (Corrected per operator: the rule never attaches without a full niko install, so reconcile-persistent *is* always present where the rule is — availability was a mis-framed concern.) The reason not to cross-reference it is direction of authority: reconcile-persistent's step 1 loads the guidance rule as the definition of what belongs in the file. A rule that pointed back at reconcile-persistent would create a cycle and leave the actual judgment homeless. Enriching the rules improves both flows with one edit: the niko path (reconcile-persistent consults a better rule) and the non-niko path (glob attachment delivers the same rule).
- **The dependency direction already points the right way.** `reconcile-persistent.md` defers to the guidance rules for *what belongs in the file* ("Load its guidance rule"). Putting the update judgment in the rules completes that design: the rules own all judgment (what belongs + when to touch), universally attached; reconcile-persistent stays a thin in-workflow trigger that consults them. Option A would invert this into a cycle.
- **The duplication B introduces is the kind this repo already treats as load-bearing.** Using reconcile-persistent's exact key phrases ("factually wrong or materially incomplete," "surgical") makes the duplication grep-verifiable, same as the consent-header pattern documented in this repo's `systemPatterns.md`.
- **The FoxForge case is out of reach of any rule amendment.** A pseudo-memory-bank inside `AGENTS.md` never attaches the `.mdc` rule. Only option D (in-file guard) touches that case — which makes D a complementary follow-on, not a competitor.
- **The ephemeral rules already model the fix.** `activeContext.mdc` and `tasks.mdc` each have a "When to Update" section; the persistent rules simply lack one. Adding it restores symmetry — persistent files get a "When to Update" whose answer is mostly "don't."

## Decision

**Selected:** Option B — inline a compact "When to Update" contract in all three persistent rules, plus an altitude test in `systemPatterns.mdc`, with option D noted as an optional follow-on for rule-less harnesses.

**Rationale (as refined by operator):** The glob rules are the single shared authority for both flows — reconcile-persistent's procedure already loads the guidance rule as the definition of what belongs, so enriching the rules improves niko and non-niko flows with one edit. The "When to Update" contract that goes into the rules is distilled, generic, and unlikely to ever drift, so it carries no real maintenance tax. No cross-reference to reconcile-persistent: not because it might be absent (it never is where the rule attaches), but because authority flows from the rules outward.

**Tradeoff:** A few sentences of generic update-contract prose appear in three rules and echo reconcile-persistent's guardrails. Accepted: the prose is generic enough to be drift-proof, and anchored on shared grep-able phrases as a tripwire.

**Operator refinements (2026-07-09):**

- Availability argument struck: the `systemPatterns.mdc` rule is never in scope without a full niko install, so reconcile-persistent is always present when it matters. The no-cross-reference conclusion stands on direction-of-authority grounds alone.
- Deliverable re-weighted: the primary work is fleshing out **what's supposed to be here** in each glob rule — especially `systemPatterns.mdc` — since that definition is what reconcile-persistent loads *and* what non-niko agents see. The "When to Update" section is the compact, generic complement, not the centerpiece.

## Implementation Notes

All edits go to canonical sources under `rulesets/niko/niko/memory-bank/` (never `.cursor/`). Per operator emphasis, the what-belongs definition (inclusion bar, altitude test, sharpened Avoid list) is the primary deliverable; the When-to-Update contract is the complement.

### `systemPatterns.mdc`

1. Rephrase the append invitation in "How to Create" — from "this document can be appended to later as actual work reveals patterns that would benefit from inclusion" to something that defers to the contract, e.g.: "Err on the side of brevity: anything omitted can be added later, under the update contract below."
2. Add a fourth "Avoid" item — the altitude test:

    > 4. Subsystem deep-dives: a detailed account of how one feature or subsystem works is a design doc, not a system pattern. The test for inclusion: would a developer working on an *unrelated* part of the system do damage without knowing this? Knowledge that only matters inside one subsystem belongs with that subsystem — its code, comments, or docs — not here.

3. Add a "When to Update" section between "How to Create" and "Format":

    > ## When to Update
    >
    > This file is read far more often than it is written, and its value is inversely proportional to its length. After creation, the default is to leave it alone: completing a task is not a reason to write here, and this file is never the place to record what you just built, fixed, or learned — that history belongs in commits, archives, and the code itself.
    >
    > Update this file only when work you just completed made something in it factually wrong or materially incomplete — and then make a surgical fix to the invalidated content, nothing more. Anything added must pass the same bar as creation: a durable, system-wide pattern at briefing altitude. When in doubt, don't: a missing pattern is cheap to add later; accumulated noise is what makes this file useless.

### `productContext.mdc`

Add a "When to Update" section:

> ## When to Update
>
> This file describes the product, not the work. After creation, the default is to leave it alone: completing a task is not a reason to write here, and a new feature does not automatically earn a mention. Update it only when work you just completed made something in it factually wrong or materially incomplete — a new user constituency, a retired use case, a changed constraint — and then make a surgical fix to the invalidated content, nothing more. When in doubt, don't.

### `techContext.mdc`

Add a "When to Update" section:

> ## When to Update
>
> After creation, the default is to leave this file alone: completing a task is not a reason to write here. Update it only when work you just completed made something in it factually wrong or materially incomplete — a build tool replaced, a test process changed, an environment step added — and then make a surgical fix to the invalidated content, nothing more. New content must pass the same bar as creation: durable pointers, not values that drift. When in doubt, don't.

### Explicitly not changed

- `reconcile-persistent.md` — stays as-is; its guardrails are procedural framing for the in-workflow pass, and it already defers to the rules for content definition. Shared key phrases contain drift.
- `archives.mdc` and the ephemeral rules — not exposed to this failure (ephemeral rules already carry "When to Update" sections).

### Follow-on Candidates

- **Option D (template guard line):** add a one-line maintenance notice to the generated persistent files themselves, so agents in rule-less harnesses (the `AGENTS.md` pseudo-memory-bank case) still see the contract. Deferred — separate decision about template shape.
- Sync propagation: after editing canonical sources, regenerate `.cursor/` / `.claude/` copies via the usual ai-rizz / a16n flow.
