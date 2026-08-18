# Decision: Plan TDD Activation

## Context

**What:** How Niko Plan should activate `always-tdd.mdc` so each executable unit in `tasks.md` is scheduled stub → red → green, explicit enough that an implementer cannot code first.

**Why it matters:** Bundling always-tdd and naming "TDD" did not produce that schedule. Preflight then patched plans in-phase (~31 stockroom incidents) until self-heal was removed, at which point the same Plan defect became a hard stop. The wrong activation leaves the FAIL shape in the template Plan agents copy. The wrong duplication forks doctrine out of `always-tdd.mdc`.

**Constraints:**
- Plan owns the schedule; always-tdd owns the doctrine. Do not restate the rule body.
- Prose/policy carve-out and change-detector ban stay.
- Preflight stays a blocking rearchitect gate (no TDD self-heal).
- Prompt-authoring: numbered list = order; bullets = a set; closed-stack pointers are allowed; restating a sibling prompt is not.
- Daz decompression keys unpack *pretrained* knowledge. always-tdd is local always-on policy. Generic "TDD red-green-refactor" *is* pretrained — Plan already used that gloss, and Daz flags reservations about that particular key. always-tdd's stubbing ritual is the novel part pretrained TDD does not contain.
- always-tdd is `alwaysApply: true`; its full text is already injected every turn. An extra Read is salience, not new information.
- Canonical edits under `rulesets/` only.

## Options Evaluated

- **A — Decompression only:** Name "always-tdd" / "red-green TDD" and trust pretrained knowledge plus always-on injection.
- **B — Explicit load:** Plan step says Read `always-tdd.mdc` immediately before writing implementation steps.
- **C — Copy the four steps into Plan:** Duplicate always-tdd's procedure into the plan docs so the agent cannot miss it.
- **D — Template-as-schedule:** Make each unit's *numbered substeps* the work (typed executable vs prose/policy). Point at always-tdd as closed-stack doctrine. Do not copy its body. Hold B in reserve.

## Analysis

| Criterion | A Name only | B Load | C Copy four steps | D Template-as-schedule |
|-----------|-------------|--------|-------------------|------------------------|
| Historical evidence | Already in production; lost. "Maps to one TDD cycle" + `Tests first:` field still emitted implementation-centric `Changes`. | alwaysApply is already a load. Stockroom plans failed with the rule in context. Load-without-structure would leave the FAIL template in place. | The current red-green-refactor *gloss* is a miniature C and already drifted off always-tdd's stubbing ritual. | Directly replaces the FAIL shape (sibling fields / preamble disclaimer) that Preflight cites. |
| Decompression-key fit | Uses the pretrained name Plan already tried. `always-tdd` has no pretraining mass, so its name can only be a pointer to a document, never a daz.is key. | Not a key; an attention move. | Rewrites the framework; Daz says that is the inferior move for established knowledge *and* we must not do it for local doctrine (drift). | Stage *names* in a numbered list refer to always-tdd contents without unpacking pretrained TDD as the ritual. Structure carries order. |
| Prompt-authoring | Disclaimer / bullet "set" | Execution handoff (allowed) | Restating a sibling (forbidden) | Numbered list = order; closed-stack pointer |
| Simplicity / reversibility | Zero new mechanism | One Read, cheap to add later | Two files of duplicated doctrine | Two plan templates; B remains a one-line follow-on |

Key insights:
- The operator's "including always-tdd was supposed to deal with that" is correct as *intent* and false as *mechanism*. Injection puts doctrine in context. It does not write `tasks.md`. The artifact the agent fills in won.
- A field named `Tests first:` encodes *membership* (this step has tests), not *sequence*. Preflight's pass condition is sequence. Workflow-prompts: bullets say order does not matter; the current template is bullets.
- Naming the four stages as numbered substep headings is not C. C is copying stubbing commentary, empty-body rules, and the change-detector paragraph. The headings are the schedule; the how stays in always-tdd.
- Load is the right *second* instrument (conserve-context: re-read instructions when adherence is the payload). It is the wrong *first* instrument: salience cannot beat a template that still looks like implementation-only steps.

## Decision

**Selected**: D — Template-as-schedule, with B held in reserve.

**Rationale:** Stockroom incidents share one planning failure: TDD declared in a preamble or label, work listed as Files + Changes (sometimes with a Tests first sibling). Preflight then expanded those units into ordered substeps. Put that expanded shape in the template Plan copies, point at always-tdd for doctrine, and stop teaching red-green-refactor in Plan's own gloss. A and C already failed or would recreate the drift. B adds no information until D is in place; if the next *executable* Plan still fails TDD encoding, add the re-read then.

**Tradeoff:** We are not adding an explicit load in this change. If structure-alone is not enough, the cheap next move is B, not another preflight band-aid.

## Implementation Notes

- In `level2-plan.md` and `level3-plan.md`, replace the "maps to roughly one TDD cycle" bullet and the `Tests first` / `Changes` sibling template with typed units (`executable` | `prose/policy`) whose executable substeps are numbered stages of `always-tdd.mdc` in order: stub tests, stub interface, write tests and run red, write code and run green. State that a step whose substeps could be reordered and still read correctly is not planned yet.
- Prose/policy units: ordered work steps plus `No tests: prose/policy artifact`. Never schedule a document change-detector.
- Keep a one-line closed-stack pointer: carve-out and process live in `always-tdd.mdc` (Niko ships it always-on). Do not paste the rule.
- Do not add "Read always-tdd.mdc" as a Plan step in this change. Record it as the follow-on if live Plans still fail encoding.
- Do not edit `niko-preflight`, `always-tdd.mdc`, L4 plan, or Build unless a wording clash appears (Build already numbers the same sequence).
- Leave `niko-plan/SKILL.md` a router.
